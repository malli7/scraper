# Job Scraper & Classifier

A comprehensive job scraping and classification system built using **FastAPI**, deployed on **Railway.app**. The application scrapes job listings from various sources, classifies them as *Entry-Level* or *Not Entry-Level* using an **XGBoost** model, and stores the data in a **Firestore database**.

## 🚀 Features

- **Job Scraping**: Extracts job listings from **Indeed, LinkedIn, and Google**.
- **Job Classification**: Uses a pre-trained **XGBoost** model to determine if a job is *Entry-Level* or *Not Entry-Level*.
- **Data Storage**: Stores job listings in a **Firestore database**.
- **API Endpoints**: Provides REST API endpoints for scraping, classifying, and retrieving job data.

## 🌐 Deployment

The application is deployed on **[Railway.app](https://job-scraper.up.railway.app/)**.

---

## 📁 Project Structure

```plaintext
.
├── app.py                  # Main FastAPI application
├── classifier.py           # Job classification logic
├── constants.py            # Application constants
├── scraper.py              # Job scraping functionality
├── storage.py              # Firestore database interactions
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
├── .env                    # Environment variables (not included in repo)
├── job_classifier_xgb.pkl  # Pre-trained XGBoost model
├── tfidf_vectorizer.pkl    # Pre-trained TF-IDF vectorizer
```

---

## 🛠 Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/malli7/scraper.git
   cd scraper
   ```

2. **Create & Activate Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the root directory.
   - Add the following credentials:
     ```env
     FIREBASE_CREDENTIALS=your_firebase_credentials_json
     ```

---

## 🚀 Usage

1. **Run the FastAPI Application**
   ```sh
   uvicorn app:app --reload
   ```

2. **Available API Endpoints**
   - **Get Jobs Count**: `GET /jobs-count`
   - **Get Job Listings**: `GET /jobs`
   - **Scrape Jobs**: `POST /scrape-jobs`

---

## 📂 Key Files

- **`app.py`** - Main FastAPI application.
- **`classifier.py`** - Job classification functions.
- **`scraper.py`** - Scrapes job listings from external sources.
- **`storage.py`** - Handles Firestore database interactions.
- **`requirements.txt`** - Python dependencies.
- **`job_classifier_xgb.pkl`** - Pre-trained XGBoost classification model.
- **`tfidf_vectorizer.pkl`** - Pre-trained TF-IDF vectorizer.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

- **[FastAPI](https://fastapi.tiangolo.com/)**
- **[Railway.app](https://railway.app/)**
- **[Firebase](https://firebase.google.com/)**
- **[Hugging Face](https://huggingface.co/)**
- **[XGBoost](https://xgboost.readthedocs.io/)**

---

## 📧 Contact

For inquiries, please contact **[mallikarjunareddygayam77@gmail.com](mailto:mallikarjunareddygayam77@gmail.com)**.

---

🚀 **Live Deployment:** [Railway.app](https://job-scraper.up.railway.app/)

