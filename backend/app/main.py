from fastapi import FastAPI 
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import SessionLocal
from app.api.routes.auth import router as auth_router
from app.api.routes.projects import router as projects_router
from app.api.routes.uploads import router as uploads_router
from app.api.routes.scans import router as scans_router

app = FastAPI(title="DevLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(uploads_router)
app.include_router(scans_router)

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
