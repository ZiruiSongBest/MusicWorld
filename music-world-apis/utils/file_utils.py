from fastapi import UploadFile
from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")

async def save_file(file: UploadFile, user_id: str):
    user_folder = UPLOAD_DIR / user_id
    user_folder.mkdir(parents=True, exist_ok=True)
    file_path = user_folder / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path