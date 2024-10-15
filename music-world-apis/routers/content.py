from fastapi import APIRouter, Request, UploadFile, File, Form
from services.SentimentAnalyzerService import sentiment_analyzer_service
from utils.file_utils import save_file, schedule_deletion
from pathlib import Path
import asyncio

router = APIRouter()

UPLOAD_DIR = Path("uploads")

@router.post("/generate")
async def generate_content(
    request: Request,
    text_prompt: str = Form(None),
    audio: UploadFile = File(None),
    image: UploadFile = File(None),
    video: UploadFile = File(None),
):
    user_id = request.cookies.get("user_id")
    audio_path = await save_file(audio, user_id) if audio else None
    image_path = await save_file(image, user_id) if image else None
    video_path = await save_file(video, user_id) if video else None

    # Schedule deletion after 24 hours
    if audio_path:
        asyncio.create_task(schedule_deletion(audio_path))
    if image_path:
        asyncio.create_task(schedule_deletion(image_path))
    if video_path:
        asyncio.create_task(schedule_deletion(video_path))

    emotion = None
    if audio_path:
        emotion = sentiment_analyzer_service.analyze(audio_path)

    return {
        # "description": description
    }


@router.get("/requests")
async def list_user_requests(request: Request):
    user_id = request.cookies.get("user_id")
    user_folder = UPLOAD_DIR / user_id
    if not user_folder.exists():
        return {"requests": []}
    files = [str(file) for file in user_folder.iterdir()]
    return {"requests": files}
