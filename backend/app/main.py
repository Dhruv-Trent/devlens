from fastapi import FastAPI

app = FastAPI(title="DevLens API")

@app.get("/")
def read_root():
    return {"message": "DevLens backend is running."}

@app.get("/health")
def health_check():
    return {"status": "ok"}