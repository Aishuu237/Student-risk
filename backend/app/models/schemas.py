from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = 'student'

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class StudentProfileUpdate(BaseModel):
    age: int
    study_time: float
    attendance: float
    assignments: float
    internet_access: bool
    extracurricular: bool

class SubjectScoreCreate(BaseModel):
    subject_name: str
    score: float
    term: str

class SubjectScoreOut(BaseModel):
    id: int
    subject_name: str
    score: float
    term: str

    class Config:
        from_attributes = True

class StudentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    avg_score: float
    attendance: Optional[float] = None
    risk_level: str
    subject_scores: List[SubjectScoreOut]
    # Profile fields (optional — present only if student has a profile)
    age: Optional[int] = None
    study_time: Optional[float] = None
    assignments: Optional[float] = None
    internet_access: Optional[bool] = None
    extracurricular: Optional[bool] = None

class StudentSummary(BaseModel):
    id: int
    name: str
    email: EmailStr
    avg_score: float
    attendance: Optional[float] = None
    risk_level: str

class PredictRequest(BaseModel):
    age: int
    study_time: float
    attendance: float
    previous_score: float
    assignments: float
    internet_access: bool
    extracurricular: bool

class FeatureImportance(BaseModel):
    feature: str
    importance: float

class PredictResponse(BaseModel):
    risk_level: str
    confidence: float
    suggestions: List[str]
    feature_importances: List[FeatureImportance]
