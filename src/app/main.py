from fastapi import FastAPI
import sys 
sys.path.append('../../')
from src.app.schema import Transaction
from app.model_loader import model, feature_columns
import numpy as np

app = FastAPI(title="Fraud Detection API")

@app.get("/")
def root():
    return {"message": "Fraud detection API is live!"}

@app.post("/predict")
def predict(transaction: Transaction):
    features = np.array([[getattr(transaction, col) for col in feature_columns]])
    proba = model.predict_proba(features)[0][1]
    if proba >0.8 : 
       return {
            "isFraud":True,
            "fraudProbability": round(float(proba), 4)
        }

    else : 
        return {
            "IsFraud": False,
            "fraudProbability": round(float(proba),4)
        }

