# 🎓 Student AI - Performance Analytics & Prediction Platform

An AI-powered web platform designed for educational institutions to monitor student performance, detect at-risk students early, and generate personalized academic predictions and improvement recommendations.

---

## 🌟 Key Features

- **📊 Student Analytics Dashboard**: Real-time visualization of attendance, study hours, assignment completion, and grade trajectories.
- **🤖 Machine Learning Grade Predictor**: Predicts final grades (G3) and identifies risk levels (High / Moderate / Low) based on academic and behavioral factors.
- **💡 AI Recommendations**: Tailored study and habit improvement suggestions generated based on individual risk profiles.
- **🛡️ Role-Based Authentication**: JWT-based secure authentication supporting both **Student** and **Admin** roles.
- **👥 Admin Management Panel**: Overview of all student records, risk distributions, and system statistics.

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: FastAPI (Python 3.10+)
- **ORM & Database**: SQLAlchemy with SQLite
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib
- **Authentication**: OAuth2 Password Bearer with JWT (python-jose, passlib/bcrypt)

### **Frontend**
- **Framework**: React 18 (Vite)
- **Styling**: Tailwind CSS & Lucide React icons
- **Charts & Data Viz**: Recharts
- **HTTP Client**: Axios with JWT interceptors

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ & npm

---

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment configuration
cp .env.example .env

# Train the ML model and seed the initial database
python app/ml/train_model.py

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

> **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

> **Frontend Application**: [http://localhost:5173](http://localhost:5173)

---

## 🔑 Demo Credentials

| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@school.com` | `admin123` |
| **Student** | `student1@school.com` | `student123` |

---

## 📁 Project Structure

```text
student-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers (auth, students, predictions)
│   │   ├── core/         # Config and security utilities
│   │   ├── models/       # SQLAlchemy database models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── ml/           # Model training and prediction logic
│   │   └── main.py       # FastAPI application entry point
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/          # Axios client & endpoints
│   │   ├── components/   # Reusable UI components & Navbar
│   │   ├── context/      # AuthContext provider
│   │   ├── pages/        # Dashboard, Prediction, Admin, Login
│   │   └── App.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
└── README.md
```
