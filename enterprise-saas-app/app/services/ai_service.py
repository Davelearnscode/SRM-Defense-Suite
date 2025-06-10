import os
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

MODEL_PATH = "ai_model.joblib"
VECTORIZER_PATH = "vectorizer.joblib"

def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
    else:
        model = MultinomialNB()
        vectorizer = CountVectorizer()
    return model, vectorizer

def save_model(model, vectorizer):
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

def predict(text):
    model, vectorizer = load_model()
    if hasattr(model, "classes_") and hasattr(vectorizer, "vocabulary_"):
        X = vectorizer.transform([text])
        return model.predict(X)[0]
    return "Unknown"

def learn(text, label):
    model, vectorizer = load_model()
    if hasattr(vectorizer, "vocabulary_"):
        X = vectorizer.transform([text])
    else:
        X = vectorizer.fit_transform([text])
    y = [label]
    if hasattr(model, "classes_"):
        model.partial_fit(X, y)
    else:
        model.partial_fit(X, y, classes=[label])
    save_model(model, vectorizer)