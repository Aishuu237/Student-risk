import os
import sys

base_dir = r"C:\Users\aishw\.gemini\antigravity\scratch\student-ai\backend"

directories = [
    "",
    "app",
    "app/models",
    "app/utils",
    "app/ml",
    "app/routers",
    "data",
    "models"
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {}

files["requirements.txt"] = """fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.35
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.1
python-multipart==0.0.12
pandas==2.2.2
scikit-learn==1.5.2
numpy==1.26.4
joblib==1.4.2
pydantic==2.9.2
pydantic-settings==2.5.2
requests==2.32.3
"""

files[".env"] = """DATABASE_URL=sqlite:///./student_ai.db
SECRET_KEY=supersecretkey_change_in_production_2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
"""

files["app/__init__.py"] = ""
files["app/models/__init__.py"] = ""
files["app/utils/__init__.py"] = ""
files["app/ml/__init__.py"] = ""
files["app/routers/__init__.py"] = ""

files["app/config.py"] = """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
"""

files["app/database.py"] = """from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

files["app/models/student.py"] = """from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default='student')
    created_at = Column(DateTime, default=datetime.utcnow)

    student_profile = relationship("Student", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    age = Column(Integer)
    study_time = Column(Float)
    attendance = Column(Float)
    assignments = Column(Float)
    internet_access = Column(Boolean)
    extracurricular = Column(Boolean)

    user = relationship("User", back_populates="student_profile")
    subject_scores = relationship("SubjectScore", back_populates="student")

class SubjectScore(Base):
    __tablename__ = "subject_scores"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_name = Column(String, index=True)
    score = Column(Float)
    term = Column(String)

    student = relationship("Student", back_populates="subject_scores")
"""

files["app/models/schemas.py"] = """from pydantic import BaseModel, EmailStr
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
"""

files["app/utils/auth.py"] = """from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.student import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = verify_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user
"""

files["app/utils/suggestions.py"] = """from typing import List

def generate_suggestions(risk_level: str, features_dict: dict) -> List[str]:
    suggestions = []
    attendance = features_dict.get('attendance', 100)
    study_time = features_dict.get('study_time', 0)
    previous_score = features_dict.get('previous_score', 0)
    assignments = features_dict.get('assignments', 0)
    internet_access = features_dict.get('internet_access', True)
    extracurricular = features_dict.get('extracurricular', False)

    if risk_level == 'HIGH':
        if attendance < 75:
            suggestions.append("Critical: Attend all classes — you're missing too many sessions. Aim for ≥85%.")
        if study_time < 1:
            suggestions.append("Start with at least 1 hour of daily focused study. Use the Pomodoro technique.")
        if previous_score < 50:
            suggestions.append("Schedule weekly tutoring sessions to strengthen fundamentals.")
        if assignments < 5:
            suggestions.append("Complete all assignments — they account for a significant grade portion.")
        if not internet_access:
            suggestions.append("Visit the school library daily for online resources and practice exercises.")
        suggestions.append("Connect with your academic counselor for a personalized recovery plan.")
    elif risk_level == 'MEDIUM':
        if attendance < 85:
            suggestions.append("Improve attendance to ≥85% — each class missed affects your understanding.")
        if study_time < 2:
            suggestions.append("Increase study time to at least 2 hours/day with structured revision.")
        if assignments < 7:
            suggestions.append("Aim to complete all assignments on time for consistent marks.")
        if not extracurricular:
            suggestions.append("Join a study group or academic club to stay motivated.")
        suggestions.append("Review weak subjects weekly and practice past papers.")
    elif risk_level == 'LOW':
        if attendance < 90:
            suggestions.append("Push attendance above 90% to secure your performance.")
        if not extracurricular:
            suggestions.append("Consider joining extracurricular activities to develop leadership skills.")
        suggestions.append("Challenge yourself with advanced problems to strengthen your understanding.")
        suggestions.append("Great work! Maintain your study routine and aim for ≥90% attendance.")

    return suggestions
"""

files["app/ml/preprocess.py"] = """import pandas as pd
import numpy as np

def load_and_prepare_data(csv_path: str):
    df = pd.read_csv(csv_path, sep=';')
    
    def get_risk(g3):
        if g3 >= 14:
            return 'LOW'
        elif g3 >= 8:
            return 'MEDIUM'
        else:
            return 'HIGH'
            
    df['risk_level'] = df['G3'].apply(get_risk)
    
    df['internet'] = df['internet'].map({'yes': 1, 'no': 0})
    df['activities'] = df['activities'].map({'yes': 1, 'no': 0})
    
    features = ['age', 'studytime', 'absences', 'G1', 'G2', 'failures', 'Dalc', 'Walc', 'internet', 'activities']
    
    # Check available columns to ensure we don't error out if some are missing
    available_features = [f for f in features if f in df.columns]
    
    X = df[available_features]
    y = df['risk_level']
    
    return X, y

def prepare_prediction_input(features_dict: dict):
    # Mapping request features to UCI features
    age = features_dict.get('age', 18)
    study_time = features_dict.get('study_time', 2.0)
    attendance = features_dict.get('attendance', 100.0)
    
    absences = round((100 - attendance) / 5)
    
    previous_score = features_dict.get('previous_score', 50.0)
    g1 = previous_score / 5
    g2 = previous_score / 5
    
    internet = 1 if features_dict.get('internet_access', True) else 0
    activities = 1 if features_dict.get('extracurricular', False) else 0
    
    failures = 0
    dalc = 1
    walc = 1
    
    # Feature order: ['age', 'studytime', 'absences', 'G1', 'G2', 'failures', 'Dalc', 'Walc', 'internet', 'activities']
    return np.array([[age, study_time, absences, g1, g2, failures, dalc, walc, internet, activities]])
"""

files["app/ml/train_model.py"] = """import os
import zipfile
import requests
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from app.ml.preprocess import load_and_prepare_data

def train():
    data_dir = os.path.join(os.path.dirname(__file__), '../../data')
    models_dir = os.path.join(os.path.dirname(__file__), '../../models')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    csv_path = os.path.join(data_dir, 'student-mat.csv')
    
    if not os.path.exists(csv_path):
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip'
        zip_path = os.path.join(data_dir, 'student.zip')
        print(f"Downloading dataset from {url}...")
        r = requests.get(url)
        with open(zip_path, 'wb') as f:
            f.write(r.content)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        print("Dataset downloaded and extracted.")

    print("Loading and preparing data...")
    X, y = load_and_prepare_data(csv_path)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    print("Saving model and metadata...")
    joblib.dump(model, os.path.join(models_dir, 'rf_model.pkl'))
    joblib.dump(X.columns.tolist(), os.path.join(models_dir, 'feature_names.pkl'))
    joblib.dump(model.classes_.tolist(), os.path.join(models_dir, 'label_classes.pkl'))
    print("Training complete.")

if __name__ == '__main__':
    # Make sure we can import from app
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    train()
"""

files["app/ml/predict.py"] = """import os
import joblib
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
    
    probabilities = model.predict_proba(input_array)[0]
    prediction = model.predict(input_array)[0]
    
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
"""

files["app/routers/auth.py"] = """from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import UserCreate, Token, UserOut
from app.models.student import User
from app.utils.auth import get_password_hash, verify_password, create_access_token

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pwd = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": UserOut.model_validate(new_user)}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": UserOut.model_validate(user)}
"""

files["app/routers/students.py"] = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.schemas import StudentOut, StudentSummary, StudentProfileUpdate, SubjectScoreCreate, SubjectScoreOut
from app.models.student import User, Student, SubjectScore
from app.utils.auth import get_current_user, get_current_admin
from app.ml.predict import predict_risk

router = APIRouter(tags=["students"])

def calculate_avg_score(scores):
    if not scores:
        return 0.0
    return sum(s.score for s in scores) / len(scores)

def get_student_details(db: Session, user: User) -> dict:
    student = user.student_profile
    if not student:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "avg_score": 0.0,
            "attendance": None,
            "risk_level": "N/A",
            "subject_scores": []
        }
        
    scores = db.query(SubjectScore).filter(SubjectScore.student_id == student.id).all()
    avg_score = calculate_avg_score(scores)
    
    try:
        features_dict = {
            "age": student.age,
            "study_time": student.study_time,
            "attendance": student.attendance,
            "previous_score": avg_score,
            "assignments": student.assignments,
            "internet_access": student.internet_access,
            "extracurricular": student.extracurricular
        }
        pred = predict_risk(features_dict)
        risk_level = pred['risk_level']
    except HTTPException:
        risk_level = "Model Not Trained"
        
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "avg_score": avg_score,
        "attendance": student.attendance,
        "risk_level": risk_level,
        "subject_scores": scores
    }

@router.get("/me", response_model=StudentOut)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_student_details(db, current_user)

@router.put("/me/profile", response_model=StudentOut)
def update_profile(profile_data: StudentProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = current_user.student_profile
    if not student:
        student = Student(user_id=current_user.id)
        db.add(student)
        
    student.age = profile_data.age
    student.study_time = profile_data.study_time
    student.attendance = profile_data.attendance
    student.assignments = profile_data.assignments
    student.internet_access = profile_data.internet_access
    student.extracurricular = profile_data.extracurricular
    
    db.commit()
    db.refresh(student)
    
    return get_student_details(db, current_user)

@router.post("/me/scores", response_model=SubjectScoreOut)
def add_score(score_data: SubjectScoreCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = current_user.student_profile
    if not student:
        raise HTTPException(status_code=400, detail="Student profile not found. Please create one first.")
        
    new_score = SubjectScore(
        student_id=student.id,
        subject_name=score_data.subject_name,
        score=score_data.score,
        term=score_data.term
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    
    return new_score

@router.get("/", response_model=List[StudentSummary], dependencies=[Depends(get_current_admin)])
def get_all_students(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.role == 'student').all()
    summaries = []
    for u in users:
        details = get_student_details(db, u)
        summaries.append(details)
    return summaries

@router.get("/{student_id}", response_model=StudentOut, dependencies=[Depends(get_current_admin)])
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == student_id, User.role == 'student').first()
    if not user:
        raise HTTPException(status_code=404, detail="Student not found")
    return get_student_details(db, user)
"""

files["app/routers/predictions.py"] = """from fastapi import APIRouter, Depends
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
"""

files["app/seed.py"] = """from sqlalchemy.orm import Session
from app.models.student import User, Student, SubjectScore
from app.utils.auth import get_password_hash

def seed_database(db: Session):
    admin = db.query(User).filter(User.email == 'admin@school.com').first()
    if admin:
        return

    admin_user = User(
        name='Admin',
        email='admin@school.com',
        hashed_password=get_password_hash('admin123'),
        role='admin'
    )
    db.add(admin_user)

    # Student 1
    s1_user = User(name='Aisha Khan', email='student1@school.com', hashed_password=get_password_hash('student123'), role='student')
    db.add(s1_user)
    db.commit()
    db.refresh(s1_user)

    s1_profile = Student(user_id=s1_user.id, age=20, study_time=3.0, attendance=87.0, assignments=8.0, internet_access=True, extracurricular=True)
    db.add(s1_profile)
    db.commit()
    db.refresh(s1_profile)
    
    s1_scores = [
        ('Python', 89, 'T1'), ('Math', 81, 'T1'), ('Physics', 73, 'T1'),
        ('Python', 91, 'T2'), ('Math', 84, 'T2'), ('Physics', 78, 'T2'),
        ('Python', 93, 'T3'), ('Math', 86, 'T3'), ('Physics', 80, 'T3')
    ]
    for sub, sc, term in s1_scores:
        db.add(SubjectScore(student_id=s1_profile.id, subject_name=sub, score=sc, term=term))

    # Student 2
    s2_user = User(name='Rahul Sharma', email='student2@school.com', hashed_password=get_password_hash('student123'), role='student')
    db.add(s2_user)
    db.commit()
    db.refresh(s2_user)
    
    s2_profile = Student(user_id=s2_user.id, age=21, study_time=1.5, attendance=65.0, assignments=5.0, internet_access=False, extracurricular=False)
    db.add(s2_profile)
    db.commit()
    db.refresh(s2_profile)
    
    s2_scores = [
        ('Math', 52, 'T1'), ('English', 61, 'T1'), ('Science', 45, 'T1'),
        ('Math', 55, 'T2'), ('English', 63, 'T2'), ('Science', 48, 'T2'),
        ('Math', 58, 'T3'), ('English', 65, 'T3'), ('Science', 50, 'T3')
    ]
    for sub, sc, term in s2_scores:
        db.add(SubjectScore(student_id=s2_profile.id, subject_name=sub, score=sc, term=term))

    # Student 3
    s3_user = User(name='Priya Patel', email='student3@school.com', hashed_password=get_password_hash('student123'), role='student')
    db.add(s3_user)
    db.commit()
    db.refresh(s3_user)

    s3_profile = Student(user_id=s3_user.id, age=19, study_time=2.5, attendance=78.0, assignments=7.0, internet_access=True, extracurricular=True)
    db.add(s3_profile)
    db.commit()
    db.refresh(s3_profile)
    
    s3_scores = [
        ('Biology', 75, 'T1'), ('Chemistry', 68, 'T1'), ('Math', 71, 'T1'),
        ('Biology', 78, 'T2'), ('Chemistry', 72, 'T2'), ('Math', 74, 'T2'),
        ('Biology', 82, 'T3'), ('Chemistry', 76, 'T3'), ('Math', 77, 'T3')
    ]
    for sub, sc, term in s3_scores:
        db.add(SubjectScore(student_id=s3_profile.id, subject_name=sub, score=sc, term=term))

    db.commit()
"""

files["app/main.py"] = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.routers import auth, students, predictions
from app.seed import seed_database
import contextlib

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(title='Student AI API', version='1.0.0', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router, prefix='/auth')
app.include_router(students.router, prefix='/students')
app.include_router(predictions.router)

@app.get("/")
def read_root():
    return {"message": "Student AI API is running"}
"""

files["run.py"] = """import subprocess
import sys
import os

if __name__ == '__main__':
    train_script = os.path.join('app', 'ml', 'train_model.py')
    subprocess.run([sys.executable, train_script])
    subprocess.run([sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'])
"""

files["README.md"] = """# Student AI Backend

## Setup
pip install -r requirements.txt

## Train Model (first time)
python app/ml/train_model.py

## Run Server
uvicorn app.main:app --reload

## API Docs
http://localhost:8000/docs

## Demo Accounts
- Admin: admin@school.com / admin123
- Student: student1@school.com / student123
"""

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Successfully created {len(files)} files in {base_dir}")
