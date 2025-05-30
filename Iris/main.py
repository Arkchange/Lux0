from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage
import os
import joblib 

app = FastAPI()

IRIS_CLASSES = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
}
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "iris_bucket010203")
MODEL_GCS_PATH = os.environ.get("MODEL_GCS_PATH", "iris-model/model.joblib")

import tempfile
MODEL_LOCAL_PATH = os.path.join(tempfile.gettempdir(), "iris_model.joblib")

model = None

class PredictionInput(BaseModel):
    features: list[float] 

class PredictionOutput(BaseModel):
    prediction: int
    label: str

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Télécharge un objet depuis un bucket."""
    print(f"Tentative de téléchargement de gs://{bucket_name}/{source_blob_name} vers {destination_file_name}...")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    try:
        blob.download_to_filename(destination_file_name)
        print(f"Fichier {source_blob_name} téléchargé vers {destination_file_name}.")
    except Exception as e:
        print(f"Erreur lors du téléchargement de {source_blob_name}: {e}")
        raise

@app.on_event("startup")
async def load_model_on_startup():
    global model
    try:
        os.makedirs(os.path.dirname(MODEL_LOCAL_PATH), exist_ok=True) 
        print("Téléchargement du modèle depuis GCS...")

        download_blob(GCS_BUCKET_NAME, MODEL_GCS_PATH, MODEL_LOCAL_PATH)

        model = joblib.load(MODEL_LOCAL_PATH)
        print("Modèle chargé avec succès en mémoire.")
    except Exception as e:
        print(f"Impossible de charger le modèle: {e}")
        model = None 
        raise RuntimeError(f"Le service n'a pas pu démarrer car le modèle n'a pas été chargé: {e}")

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé ou service indisponible.")

    try:
        features_array = [input_data.features] 

        prediction = int(model.predict(features_array)[0])

        label = IRIS_CLASSES.get(prediction, "unknown")
        output = PredictionOutput(prediction=prediction, label=label)
        print("Valeur retournée :", output.dict())
        return output
    except Exception as e:
        print(f"Erreur lors de la prédiction: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {e}")

@app.get("/health")
async def health_check():
    if model is not None:
        return {"status": "ok", "model_loaded": True}
    else:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
