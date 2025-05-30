import spacy
import joblib
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from google.cloud import storage
import tempfile
import re
import os

app = FastAPI()
nlp = spacy.load("fr_core_news_sm")


def download_model_gcs(blop_name: str):
    # Télécharge un objet depuis un bucket GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket("cand_bucket")
    blob = bucket.blob(blop_name)
    tmp_file = tempfile.NamedTemporaryFile(delete = False)
    blob.download_to_filename(tmp_file.name)
    return tmp_file.name

try:
    model_path = download_model_gcs("Candidature.joblib")
    vectorizer_path = download_model_gcs("vectorizer.joblib")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    os.remove(model_path)
    os.remove(vectorizer_path)
    print("Modèles chargés et fichiers temporaires supprimés.")
except Exception as e:
    print(f"Erreur lors du chargement des modèles : {e}")
    model = None
    vectorizer = None


def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])


# Donnée attendue pour la prédiction
class PredictionInput(BaseModel):
    features: List[str]

@app.post("/predict")
def predict(input_data: PredictionInput):

    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Modèles non chargés. Vérifiez le log du démarrage.")

    try:
        cleaned_texts = [preprocess(text) for text in input_data.features]
        X = vectorizer.transform(cleaned_texts)
        predictions = model.predict(X)
        print("cleaned_texts:", cleaned_texts)
        return {"predictions": predictions.tolist()}
    except Exception as e :
        raise HTTPException(status_code=400, detail=f"Erreur lors de la prédiction: {str(e)}")

@app.get("/health")
async def health_check():
    if model is not None and vectorizer is not None and nlp is not None:
        return {"status": "ok", "model_loaded": True, "vectorizer_loaded": True, "nlp_loaded": True}
    else:
        raise HTTPException(status_code=503, detail="Composant manquant")
