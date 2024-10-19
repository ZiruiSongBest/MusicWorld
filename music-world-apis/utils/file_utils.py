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

async def save_multiple_files(files: list[UploadFile], user_id: str) -> list[Path]:
    paths = []
    for file in files:
        path = await save_file(file, user_id)
        paths.append(path)
    return paths


async def schedule_deletion(file_path: Path | str, delay: int = 10000):
    await asyncio.sleep(delay)
    path = Path(file_path) if isinstance(file_path, str) else file_path
    if path.exists():
        path.unlink()
