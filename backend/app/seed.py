from sqlalchemy.orm import Session
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
