# 🧠 Job Scraper & Classifier API

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/XGBoost-ML-orange?style=for-the-badge&logo=machine-learning" alt="XGBoost" />
  <img src="https://img.shields.io/badge/Firestore-Database-yellow?style=for-the-badge&logo=firebase" alt="Firestore" />
  <img src="https://img.shields.io/badge/Deployed-Railway-black?style=for-the-badge&logo=railway" alt="Railway" />
</div>

<br/>

<div align="center">
  <h3>🔍 Intelligent Job Scraping & Classification API</h3>
  <p>A high-performance backend system that scrapes, classifies, and serves job listings with machine learning integration.</p>
</div>

---

## 📋 Overview

The **Job Scraper & Classifier API** is a scalable backend service built with **FastAPI** that automates the collection and classification of job postings. Designed for academic and real-world deployment scenarios, it scrapes jobs from top platforms (Indeed, LinkedIn, Google Jobs), classifies them using a trained **XGBoost model**, and stores clean, structured data in **Google Firestore**. 

This microservice is ideal for powering job discovery platforms, analytics dashboards, or machine learning pipelines focused on entry-level job market research.

---

## ✨ Key Features

<table>
  <tr>
    <td width="50%">
      <h3>🕷️ Automated Job Scraping</h3>
      <ul>
        <li>Supports Indeed, LinkedIn, and Google Jobs</li>
        <li>Customizable and extendable scraping logic</li>
        <li>Removes duplicates and enriches metadata</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🧠 Entry-Level Classification</h3>
      <ul>
        <li>Pre-trained <strong>XGBoost</strong> model</li>
        <li><strong>TF-IDF</strong> vectorization of job descriptions</li>
        <li>Binary classification: Entry-Level / Not Entry-Level</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>☁️ Firestore Integration</h3>
      <ul>
        <li>Structured NoSQL job listings storage</li>
        <li>Queryable collections with indexing</li>
        <li>Metadata for company, location, tags</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🛠️ RESTful API Endpoints</h3>
      <ul>
        <li>Trigger scraping jobs manually</li>
        <li>Access job count and records</li>
        <li>Secure and scalable with FastAPI</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🌐 Live Deployment

> **🚀 Hosted on Railway:**  
> 🌍 [https://job-scraper.up.railway.app/](https://job-scraper.up.railway.app/)

---

## 📂 Project Structure

```
job_scraper_classifier/
├── app.py                  # FastAPI application entry point
├── scraper.py              # Scraper logic for multiple sources
├── classifier.py           # XGBoost model + TF-IDF based classifier
├── storage.py              # Firestore interaction layer
├── constants.py            # Source URLs and config variables
├── job_classifier_xgb.pkl  # Pre-trained XGBoost model
├── tfidf_vectorizer.pkl    # Pre-trained TF-IDF vectorizer
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not tracked)
└── README.md               # Project documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10+
- Virtual Environment (recommended)
- Firebase project & credentials
- Railway.app account (optional for deployment)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/malli7/scraper.git
   cd scraper
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory and add:
   ```env
   FIREBASE_CREDENTIALS=your_firebase_credentials_json
   ```

---

## 🚀 Running the Application

Start the FastAPI server with:

```bash
uvicorn app:app --reload
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

---

## 🔌 API Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/jobs`            | Retrieve all classified job listings |
| GET    | `/jobs-count`      | Get total count of stored jobs       |
| POST   | `/scrape-jobs`     | Trigger job scraping & classification|

---

## 🧠 ML Model Details

- **Model**: XGBoost Classifier
- **Vectorizer**: TF-IDF with stopword removal
- **Input**: Raw job description text
- **Output**: Binary classification (`Entry-Level`, `Not Entry-Level`)

Models are pre-trained and loaded at runtime from `.pkl` files.

---

## 🧩 Future Enhancements

- [ ] Scheduled scraping via CRON or Cloud Functions  
- [ ] Admin dashboard to manage job sources  
- [ ] Confidence scoring and soft classification  
- [ ] Integration with resume matching module

---

## 🧪 Technologies Used

- **FastAPI** – High-performance web framework
- **XGBoost** – Robust ML classification engine
- **TF-IDF** – Text vectorization for NLP
- **Google Firestore** – Cloud-native NoSQL storage
- **Railway.app** – Simple, fast deployment platform

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>Built for developers, researchers, and innovators working on next-gen job platforms.</p>
  <p>© 2025 Job Scraper & Classifier API</p>
</div>
