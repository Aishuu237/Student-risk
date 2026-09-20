from fastapi import APIRouter, Depends, HTTPException
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
        "subject_scores": scores,
        "age": student.age,
        "study_time": student.study_time,
        "assignments": student.assignments,
        "internet_access": student.internet_access,
        "extracurricular": student.extracurricular,
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
