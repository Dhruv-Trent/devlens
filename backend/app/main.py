from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import SessionLocal

app = FastAPI(title="DevLens API")

@app.get("/")
def read_root():
    return {"message": "DevLens backend is running."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/db-test")
def db_test():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected"}
    finally:
        db.close()


