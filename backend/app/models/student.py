from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
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
