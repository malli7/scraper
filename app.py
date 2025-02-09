from fastapi import FastAPI
from typing import Optional
import pandas as pd
from scraper import scrape_jobs_async
from classifier import classify_jobs
from storage import count_documents,save_large_dataset_to_firestore,get_all_jobs
from constants import JOB_ROLES 
from datetime import datetime, timedelta
import asyncio
from bot2 import classify_job_with_model


app = FastAPI()

@app.get('/jobs-count')
async def old_api():
    return count_documents("jobs") 

@app.get('/jobs')
def get_jobs():
    x =  get_all_jobs("jobs")
    print(x.head())
    return x


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
        
        #classifications = await process_jobs_in_batches(filtered_jobs)
        classifications =  classify_jobs(filtered_jobs)
        filtered_jobs["entry_level"] = classifications
        filtered_jobs["date_posted"] = filtered_jobs["date_posted"].fillna(pd.to_datetime(datetime.today().strftime('%Y-%m-%d'), errors='coerce').date())
        filtered_jobs["date_posted"] = pd.to_datetime(filtered_jobs["date_posted"], errors="coerce").dt.date
        filtered_jobs = filtered_jobs[filtered_jobs['date_posted'] >= specified_date]
        filtered_jobs.replace({pd.NA: None}, inplace=True)
        filtered_jobs = pd.DataFrame(filtered_jobs) 
        entry_level_jobs = filtered_jobs.loc[filtered_jobs['entry_level'] =="Entry-Level"].copy()
        print("entry Jobs:", filtered_jobs['entry_level'].value_counts())
        
        a = await save_large_dataset_to_firestore(entry_level_jobs, 'jobs')
        
        
        await asyncio.sleep(2)  
    
    return {'message':"No jobs found"} if entry_level_jobs['entry_level'].nunique() == 0 else {"message": a}
