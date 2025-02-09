import pickle
import pandas as pd

with open("job_classifier_xgb.pkl", "rb") as model_file:
    loaded_model = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
    loaded_vectorizer = pickle.load(vectorizer_file)

def classify_job_with_model(title, description):
    """Classifies a job as Entry-Level or Not Entry-Level."""
    job_text = title + " " + description
    job_tfidf = loaded_vectorizer.transform([job_text])
    prediction = loaded_model.predict(job_tfidf)[0]
    return "Entry-Level" if prediction == 0 else "Not Entry-Level"

def classify_jobs(jobs):
    """Classifies a list of jobs dynamically, converting DataFrame if necessary."""
    if isinstance(jobs, pd.DataFrame):
        jobs = jobs.to_dict(orient='records')  
    
    if not isinstance(jobs, list) or not all(isinstance(job, dict) for job in jobs):
        raise TypeError(f"Expected jobs to be a list of dictionaries, but got {type(jobs)}")
    
    results = [classify_job_with_model(job["title"], job["description"]) for job in jobs]
    counts = {"Entry-Level": results.count("Entry-Level"), "Not Entry-Level": results.count("Not Entry-Level")}
    return results


