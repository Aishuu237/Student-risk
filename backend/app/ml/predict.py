import os
import joblib
import pandas as pd
from fastapi import HTTPException
from app.ml.preprocess import prepare_prediction_input

model = None
feature_names = None
label_classes = None

def load_model():
    global model, feature_names, label_classes
    if model is not None:
        return
        
    models_dir = os.path.join(os.path.dirname(__file__), '../../models')
    model_path = os.path.join(models_dir, 'rf_model.pkl')
    
    if not os.path.exists(model_path):
        raise HTTPException(status_code=503, detail="Model not trained yet. Run train_model.py first.")
        
    model = joblib.load(model_path)
    feature_names = joblib.load(os.path.join(models_dir, 'feature_names.pkl'))
    label_classes = joblib.load(os.path.join(models_dir, 'label_classes.pkl'))

def predict_risk(features_dict: dict) -> dict:
    load_model()
    
    input_array = prepare_prediction_input(features_dict)
    input_df = pd.DataFrame(input_array, columns=feature_names)
    
    probabilities = model.predict_proba(input_df)[0]
    prediction = model.predict(input_df)[0]
    
    confidence = max(probabilities) * 100
    
    importances = model.feature_importances_
    feature_importances = [
        {"feature": name, "importance": float(imp)}
        for name, imp in zip(feature_names, importances)
    ]
    feature_importances.sort(key=lambda x: x['importance'], reverse=True)
    
    return {
        "risk_level": str(prediction),
        "confidence": float(confidence),
        "feature_importances": feature_importances
    }
