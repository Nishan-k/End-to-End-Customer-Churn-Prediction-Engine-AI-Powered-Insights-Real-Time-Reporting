from fastapi import FastAPI, Request, HTTPException
import joblib
import pandas as pd
from api.schemas import Input_features
# from src.components.charts import create_clean_shap_dashboard
import streamlit as st


# Load the saved model:
model = joblib.load("ml/churn_clf_model.pkl")



app = FastAPI()
@app.get("/")
def landing_page():
    return "Hello there!!"


# Make the prediction:
@app.post("/predict")
def predict_churn(input_features:Input_features):
    try:
        input_data = pd.DataFrame([input_features.model_dump()])
        result = model.predict(input_data)
        pred_prob = model.predict_proba(input_data)
        pred_prob = pred_prob[0][pred_prob.argmax()]
        prediction = result.tolist()[0]
        return {"Prediction": prediction, "Prediction_proba": pred_prob}
    
    except Exception as e:
        return {'error': str(e)}


# @app.post("/explain")
# async def explain_shap():
#     result = create_clean_shap_dashboard(customer_data=customer_data, model=model)
#     return result