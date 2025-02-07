import asyncio
from jobspy import scrape_jobs

async def scrape_jobs_async(search, location, resultcount):
    try:
        return await asyncio.to_thread(
            scrape_jobs,
            site_name=["indeed", "linkedin", "google"],
            search_term=search,
            google_search_term=f"{search} jobs near {location} in United States since yesterday",
            location=location,
            results_wanted=int(resultcount),
            hours_old=24,
            country_indeed="USA",
            linkedin_fetch_description=True,
            experience_level=["entry_level"],

        )
    except Exception as e:
        print(f"Error occurred: {e}") 
        return None 
