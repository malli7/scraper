import os
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json

if not firebase_admin._apps:
    firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
    firebase_secrets = json.loads(firebase_creds.replace("\n", "\\n"))
    cred = credentials.Certificate(firebase_secrets)
    #cred = credentials.Certificate("./serviceAccountKey.json") 
    firebase_admin.initialize_app(cred)

db = firestore.client()


def convert_firestore_compatible(data):
    for key, value in data.items():
        if isinstance(value, datetime.date):
            data[key] = datetime.datetime.combine(value, datetime.datetime.min.time())
    return data


async def save_large_dataset_to_firestore(jobs_df, collection_name, batch_size=400):
    await delete_old_records("jobs", days_old=3)
    if jobs_df.empty:
        print("Dataset is empty. No data to upload.")
        return
    
    total_records = len(jobs_df)
    print(f"Uploading {total_records} records to Firestore in batches...")

    for i in range(0, total_records, batch_size):
        batch = db.batch()
        chunk = jobs_df.iloc[i:i+batch_size]  

        for _, row in chunk.iterrows():
            job_id = row["id"]  
            doc_ref = db.collection(collection_name).document(job_id)
            job_data = convert_firestore_compatible(row.to_dict())
            batch.set(doc_ref, job_data)

        batch.commit()
        print(f"Uploaded batch {i+1}-{min(i+batch_size, total_records)} successfully.")

    print("🔥 All records have been uploaded successfully!")
    return (f"Uploading {total_records} records to Firestore in batches...")
    


async def delete_old_records(collection_name, date_field="date_posted", days_old=3):
    
    today = datetime.datetime.utcnow()
    threshold_date = today - datetime.timedelta(days=days_old)

    docs = db.collection(collection_name).stream()
    deleted_count = 0
    for doc in docs:
        data = doc.to_dict()

        if date_field in data:
            try:
                date_posted = data[date_field]
                if isinstance(date_posted, str):
                    date_posted = datetime.datetime.strptime(date_posted, "%Y-%m-%d")
                elif isinstance(date_posted, firestore.SERVER_TIMESTAMP):
                    date_posted = date_posted.to_datetime()

                if date_posted < threshold_date:
                    db.collection(collection_name).document(doc.id).delete()
                    deleted_count += 1
                    print(f"Deleted {doc.id} (Posted: {date_posted})")

            except Exception as e:
                continue

    print(f"✅ Deleted {deleted_count} old records from {collection_name}.")



def count_documents(collection_name):
    docs = db.collection(collection_name).stream()
    count = sum(1 for _ in docs)  
    print(f"Total records in '{collection_name}': {count}")
    return count



def get_all_jobs(collection_name):
    try:
        docs = db.collection(collection_name).stream()
        jobs_list = [doc.to_dict() for doc in docs]
        jobs_df = pd.DataFrame(jobs_list)

        if jobs_df.empty:
            print("No jobs found in the collection.")
        else:
            print(f"Retrieved {len(jobs_df)} job records successfully.")

        jobs_df = jobs_df.replace({np.nan: None})
        jobs_df.to_csv("jobs.csv", index=False)
        return jobs_df

    except Exception as e:
        print(f"Error retrieving jobs: {e}")
        return pd.DataFrame()  
