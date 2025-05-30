import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import spacy
import joblib

df = pd.read_csv('Candidature.csv', encoding='utf-8')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Tokenization
    return text

for text in df['Contenu']:
    preprocessed_text = preprocess_text(text)
    df['Contenu'] = df['Contenu'].replace(text, preprocessed_text)

nlp = spacy.load("fr_core_news_sm")

def spacy_tokenizer(text):
    doc = nlp(text.lower())
    return " ".join([token.text for token in doc if not token.is_stop and not token.is_punct])

df["Contenu_Lemmatise"] = df["Contenu"].apply(spacy_tokenizer)

# Exemple de dataset
X = df["Contenu_Lemmatise"]
y = df["Réponse"]

X_train, X_test, y_train, y_test =X[8:], X[:8],y[8:], y[:8] #First 8 cause true labels other are GPT

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train_vec, y_train)

#y_pred = model.predict(X_test_vec)

#print("Classification Report:\n", classification_report(y_test, y_pred))

joblib.dump(model, "Candidature.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")