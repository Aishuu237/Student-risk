from fastapi import FastAPI
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/auth')
app.include_router(students.router, prefix='/students')
app.include_router(predictions.router)

@app.get("/")
def read_root():
    return {"message": "Student AI API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
