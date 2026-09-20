from fastapi import APIRouter, Depends
from app.models.schemas import PredictRequest, PredictResponse
from app.utils.auth import get_current_user
from app.models.student import User
from app.ml.predict import predict_risk
from app.utils.suggestions import generate_suggestions

router = APIRouter(tags=["predictions"])

@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest, current_user: User = Depends(get_current_user)):
    features_dict = request.model_dump()
    
    prediction = predict_risk(features_dict)
    suggestions = generate_suggestions(prediction["risk_level"], features_dict)
    
    return {
        "risk_level": prediction["risk_level"],
        "confidence": prediction["confidence"],
        "suggestions": suggestions,
        "feature_importances": prediction["feature_importances"]
    }
