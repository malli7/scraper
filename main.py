from fastapi import FastAPI
from typing import Optional
from jobspy import scrape_jobs
import sys
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Define the classification function
def classify_job(job_title, job_description):
    prompt = f"""
    You are an AI trained to classify job descriptions as "Entry-Level" or "Not Entry-Level."

    **Classification Criteria:**
    
    1. **Entry-Level** if:
       - **Experience:**
         - Requires **0-2 years** of experience or explicitly states "No prior experience required."
         - Mentions terms like **"internship," "recent graduates,"** or indicates **training/mentorship** will be provided.
       - **Responsibilities:**
         - Involves **basic tasks**, **assisting senior staff**, or roles focused on **learning and development**.
         - Tasks are **clearly defined** with **supervision** and **guidance**.
       - **Skills:**
         - Requires **foundational knowledge** in relevant fields.
         - Seeks **proficiency in common tools** or technologies pertinent to the role.
         - Emphasizes **soft skills** such as **communication**, **teamwork**, and **adaptability**.
       - **Current Market Trends:**
         - Aligns with **emerging roles** in sectors like **technology**, **green energy**, or **healthcare**.
         - Reflects the **rise of remote work** and **flexible working conditions**.
    
    2. **Not Entry-Level** if:
       - **Experience:**
         - Requires **3 or more years** of experience.
         - Expects candidates to have **prior industry experience** or **specialized certifications**.
       - **Responsibilities:**
         - Involves **independent project ownership**, **leadership**, or **management** roles.
         - Requires **strategic decision-making** or **oversight** of significant projects.
       - **Skills:**
         - Demands **advanced technical expertise** or **specialized knowledge**.
         - Requires **proficiency in multiple advanced tools** or **technologies**.
         - Expects **proven track records** of **problem-solving** and **innovation**.
       - **Current Market Trends:**
         - Pertains to **established roles** with **stable demand**.
         - Less emphasis on **flexibility** or **emerging sectors**.

    **Classification Task:**
    
    Given the following job details:
    - **Job Title**: {job_title}
    - **Job Description**: {job_description}
    
    Respond with **only one of two possible outputs**:
    1. "Entry-Level"
    2. "Not Entry-Level"
    
    Do not provide any explanation; just return one of these two outputs.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a job classification assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0,  # To ensure deterministic output
        max_tokens=10
    )
   
    return response.choices[0].message.content











app = FastAPI()

@app.get("/python-version")
async def python_version():
    return {"python_version": sys.version}

@app.get("/scrape-jobs")
async def scrape_jobs_api(
    search: Optional[str] = "software engineer",
    location: Optional[str] = "San Francisco, CA",
    resultcount: Optional[str] = 5,
):
    jobs = scrape_jobs(
        site_name=["linkedin"],
        search_term=search,
        google_search_term=f"{search} jobs near {location} since yesterday",
        location=location,
        results_wanted=int(resultcount),
        hours_old=24,
        country_indeed="USA",
        linkedin_fetch_description=True,
    )

    filtered_jobs = jobs[
        [
            "id",
            "site",
            "job_url",
            "job_url_direct",
            "title",
            "company",
            "location",
            "job_type",
            "job_level",
            "job_function",
            "emails",
            "description",
            "company_url",
        ]
    ]


    job_data_dict = filtered_jobs.to_dict(orient="records")  # List of dictionaries

    for job in job_data_dict:
        title = job["title"]
        description = job["description"]
        classification = classify_job(title, description)
        filtered_jobs['entry_level'] = classification
        print(f"Title: {title},classification: {classification}")
    
    

    return filtered_jobs.to_dict(orient="records")


