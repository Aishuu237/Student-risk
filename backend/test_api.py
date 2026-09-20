import requests

BASE = 'http://127.0.0.1:8000'

# 1. Health
r = requests.get(f'{BASE}/')
print('Health:', r.status_code, r.json())

# 2. Login Student
r = requests.post(f'{BASE}/auth/login', data={'username': 'student1@school.com', 'password': 'student123'})
print('Student login:', r.status_code)
student_token = r.json()['access_token']
s_headers = {'Authorization': f'Bearer {student_token}'}

# 3. Student /me
r = requests.get(f'{BASE}/students/me', headers=s_headers)
me = r.json()
print('Student profile:', me['name'], 'Avg Score:', me['avg_score'], 'Risk:', me['risk_level'])

# 4. Predict
pred_data = {
    'age': 20,
    'study_time': 3.0,
    'attendance': 82.0,
    'previous_score': 74.0,
    'assignments': 8.0,
    'internet_access': True,
    'extracurricular': True
}
r = requests.post(f'{BASE}/predict', json=pred_data, headers=s_headers)
pred = r.json()
print('Predict:', pred['risk_level'], 'Conf:', round(pred['confidence'], 1), '%')
print('Top Factor:', pred['feature_importances'][0])
print('Suggestions count:', len(pred['suggestions']))

# 5. Login Admin
r = requests.post(f'{BASE}/auth/login', data={'username': 'admin@school.com', 'password': 'admin123'})
print('Admin login:', r.status_code)
admin_token = r.json()['access_token']
a_headers = {'Authorization': f'Bearer {admin_token}'}

# 6. Admin All Students
r = requests.get(f'{BASE}/students/', headers=a_headers)
students = r.json()
print('Admin total students found:', len(students))
for s in students:
    name = s['name']
    avg = s['avg_score']
    att = s['attendance']
    risk = s['risk_level']
    print(f' - {name}: Avg={avg:.1f}%, Attendance={att}%, Risk={risk}')
