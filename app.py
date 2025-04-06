from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import pandas as pd
from scraper import scrape_jobs_async
from classifier import classify_jobs
from storage import count_documents,save_large_dataset_to_firestore,get_paginated_jobs,delete_old_records
from constants import JOB_ROLES 
from datetime import datetime, timedelta
import asyncio
from resume_score import calculate_score
from fastapi.responses import JSONResponse

from pydantic import BaseModel

# Define a Pydantic model for the request body
class EvaluationRequest(BaseModel):
    job_description: str
    resume_text: str

app = FastAPI()

@app.get('/jobs-count')
async def old_api():
    return count_documents("jobs") 

@app.get('/delete')
async def delete_old_records_route(
    days_old: int = Query(3, description="Number of days old to delete records")
):
    await delete_old_records("jobs", days_old=days_old)
    return {"message": f"Deleted records older than {days_old} days"}



@app.get('/paginated-jobs')
def get_paginated_jobs_route(
    page_size: int = Query(10, description="Number of jobs per page"),
    page_number: int = Query(1, description="Page number to retrieve")
):
    jobs_df = get_paginated_jobs("jobs", page_size, page_number)
    if jobs_df.empty:
        return JSONResponse(content={"message": "No jobs found"}, status_code=404)
    
    # Convert Timestamp objects to strings
    jobs_df['date_posted'] = jobs_df['date_posted'].astype(str)
    return JSONResponse({"content":jobs_df.to_dict(orient='records')})


@app.post("/evaluate-resume")
async def evaluate_resume_route(request: EvaluationRequest):
    try:
        result = calculate_score(request.job_description, request.resume_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/scrape-jobs")
async def scrape_jobs_api(
    search: Optional[str] = None,
    location: Optional[str] = "United States",
    resultcount: Optional[int] = 5,
):
    search_terms = JOB_ROLES if search is None else [search]
    specified_date = pd.to_datetime((datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d'), errors='coerce').date()
    
    for role in search_terms:
        jobs = await scrape_jobs_async(role, location, resultcount)
        if jobs is None or jobs.empty:
            await asyncio.sleep(2)  
            continue
        
        filtered_jobs = jobs[
            ["id", "site", "job_url", "job_url_direct", "title", "company", "location", "job_type", "description", "company_url", "date_posted"]
        ].copy()
        
        classifications =  classify_jobs(filtered_jobs)
        filtered_jobs["entry_level"] = classifications
        filtered_jobs.drop_duplicates(subset=["id"], inplace=True)
        filtered_jobs.dropna(subset=["id","title", "entry_level", "description"], inplace=True)
        filtered_jobs["date_posted"] = filtered_jobs["date_posted"].fillna(
            pd.to_datetime(datetime.today().strftime('%Y-%m-%d'), errors='coerce').date()
        )
        filtered_jobs["date_posted"] = pd.to_datetime(filtered_jobs["date_posted"], errors="coerce").dt.tz_localize('UTC').dt.date
        filtered_jobs = filtered_jobs[filtered_jobs['date_posted'] >= specified_date]
        filtered_jobs.replace({pd.NA: None}, inplace=True)
        filtered_jobs = pd.DataFrame(filtered_jobs) 
        
        filtered_jobs["category"] = role
        
        entry_level_jobs = filtered_jobs.loc[filtered_jobs['entry_level'] =="Entry-Level"].copy()
        print("entry Jobs:", filtered_jobs['entry_level'].value_counts())
        
        a = await save_large_dataset_to_firestore(entry_level_jobs, 'jobs')
        
        
        await asyncio.sleep(2)  
    
    return {'message':"No jobs found"} if entry_level_jobs['entry_level'].nunique() == 0 else {"message": a}
