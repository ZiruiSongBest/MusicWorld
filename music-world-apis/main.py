from fastapi import FastAPI
from app.api import upload, preprocess, analyze, response

app = FastAPI()

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(preprocess.router, prefix="/preprocess", tags=["preprocess"])
app.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
app.include_router(response.router, prefix="/response", tags=["response"])

@app.get("/")
def read_root():
    return {"message": "Music World APIs"}