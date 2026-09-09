import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# Load processed data
df = pd.read_csv("data/processed_incidents.csv")

# Remove missing values
df = df.dropna(subset=["text", "category"])

X = df["text"]
y = df["category"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# Build ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )),
    ("classifier", LogisticRegression(
        max_iter=1000
    ))
])


# Train model
model.fit(X_train, y_train)


# Save model
joblib.dump(model, "models/incident_classifier.pkl")


print("Model trained successfully.")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Model saved to models/incident_classifier.pkl")