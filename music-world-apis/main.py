from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import content

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(content.router)

# uvicorn main:app --reload