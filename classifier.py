import asyncio
from openai import OpenAI
from constants import OPENAI_API_KEY, BATCH_SIZE

client = OpenAI(api_key=OPENAI_API_KEY)

async def classify_job(job_title, job_description):
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

    response = await asyncio.to_thread(
        client.chat.completions.create,
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a job classification assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=5
    )

    return response.choices[0].message.content.strip()

async def process_jobs_in_batches(jobs):
    results = []
    
    for i in range(0, len(jobs), BATCH_SIZE):
        batch = jobs[i : i + BATCH_SIZE]
        tasks = [classify_job(job["title"], job["description"]) for _, job in batch.iterrows()]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
        await asyncio.sleep(2)
    
    cleaned_list = [item.strip('"') for item in results]
    return cleaned_list

