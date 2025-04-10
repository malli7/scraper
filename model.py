import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

file_path = "a.csv"
df = pd.read_csv(file_path, encoding="utf-8")

df = df.fillna("Unknown")

if "title" in df.columns and "description" in df.columns and "entry_level" in df.columns:
    df_filtered = df[["title", "description"]].astype(str).agg(' '.join, axis=1)
    labels = df["entry_level"].map({"Entry-Level": 0, "Not Entry-Level": 1})
    df_filtered, labels = df_filtered[labels.notna()], labels.dropna()
else:
    raise ValueError("Dataset missing required columns: 'title', 'description', 'entry_level'")

labels = labels.astype(int)

df_filtered, labels = df_filtered.align(labels, join='inner')

X_train, X_test, y_train, y_test = train_test_split(
    df_filtered, labels, test_size=0.2, random_state=42, stratify=labels
)

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = xgb.XGBClassifier(
    max_depth=20, 
    n_estimators=400, 
    eval_metric='logloss', 
    scale_pos_weight=len(y_train[y_train == 0]) / len(y_train[y_train == 1]) 
)


model.fit(X_train_tfidf, y_train)

with open("job_classifier_xgb2.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("tfidf_vectorizer2.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred, target_names=["Entry-Level", "Not Entry-Level"])
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(classification_rep)