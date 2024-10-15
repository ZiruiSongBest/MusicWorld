from fastapi import UploadFile
from pathlib import Path
import shutil
import asyncio

UPLOAD_DIR = Path("uploads")


async def save_file(file: UploadFile, user_id: str):
    user_folder = UPLOAD_DIR / user_id
    user_folder.mkdir(parents=True, exist_ok=True)
    file_path = user_folder / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


async def schedule_deletion(file_path: Path, delay: int = 2000):
    await asyncio.sleep(delay)
    if file_path.exists():
        file_path.unlink()
