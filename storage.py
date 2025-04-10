import os
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json
import pytz

if not firebase_admin._apps:
    firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
    firebase_secrets = json.loads(firebase_creds.replace("\n", "\\n"))
    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def convert_firestore_compatible(data):
    for key, value in data.items():
        if isinstance(value, datetime.date):
            data[key] = datetime.datetime.combine(value, datetime.datetime.min.time())
    return data


async def save_large_dataset_to_firestore(jobs_df, collection_name, batch_size=400):
    current_time = datetime.datetime.now().time()
    if current_time >= datetime.time(14, 0) and current_time < datetime.time(15, 0):
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
    today = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    threshold_date = today - datetime.timedelta(days=days_old)

    docs = db.collection(collection_name).stream()
    deleted_count = 0

    for doc in docs:
        data = doc.to_dict()

        if date_field in data:
            try:
                date_posted = data[date_field]

                # Normalize date_posted to UTC and ensure it's in YYYY-MM-DD format
                if isinstance(date_posted, str):
                    date_posted = datetime.datetime.strptime(date_posted, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
                elif isinstance(date_posted, datetime.datetime):
                    if date_posted.tzinfo is None:
                        date_posted = date_posted.replace(tzinfo=pytz.UTC)
                elif isinstance(date_posted, datetime.date):
                    date_posted = datetime.datetime.combine(date_posted, datetime.datetime.min.time()).replace(tzinfo=pytz.UTC)
                else:
                    continue

                # Perform comparison
                if date_posted < threshold_date:
                    db.collection(collection_name).document(doc.id).delete()
                    deleted_count += 1

            except Exception as e:
                print(f"Error processing document {doc.id}: {e}")
                continue

    print(f"✅ Deleted {deleted_count} old records from {collection_name}.")


def count_documents(collection_name):
    docs = db.collection(collection_name).stream()
    count = sum(1 for _ in docs)  
    print(f"Total records in '{collection_name}': {count}")
    return count

