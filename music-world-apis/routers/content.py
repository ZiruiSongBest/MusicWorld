from fastapi import APIRouter, Request, UploadFile, File, Form
from services.AudioAnalyzerService import AudioAnalyzerService, audio_analyzer_service
from services.AudioGeneratorService import AudioGenerator, audio_generator_service
from services.PromptService import PromptService, prompt_service
from utils.file_utils import save_file, schedule_deletion
from pathlib import Path
from typing import Optional
import asyncio
from fastapi.responses import StreamingResponse

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

    # Save uploaded files
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
        emotion = audio_analyzer_service.analyze(audio_path)
        audio_information = prompt_service.analyze_audio_file(audio_path, emotion)

    # generate audio
    generated_audio = audio_generator_service.generate_audio(
        text_prompt
    )

    description = prompt_service.create_prompt(
        text_prompt=text_prompt,
        emotion=emotion,
    )

    user_folder = UPLOAD_DIR / user_id
    generated_audio_path = user_folder / "generated_audio.mp3"

    with open(generated_audio_path, "wb") as f:
        f.write(generated_audio)

    # with open(album_image_path, "wb") as f:
    #     f.write(album_image)

    asyncio.create_task(schedule_deletion(generated_audio_path))
    # asyncio.create_task(schedule_deletion(album_image_path))

    def iterfile():
        with open(generated_audio_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="audio/mpeg")

    # base_url = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}"
    # audio_url = f"{base_url}/uploads/{user_id}/generated_audio.mp3"
    # return {
    #     "audio_url": audio_url,
    # }


@router.get("/requests")
async def list_user_requests(request: Request):
    user_id = request.cookies.get("user_id")
    user_folder = UPLOAD_DIR / user_id
    if not user_folder.exists():
        return {"requests": []}
    files = [str(file) for file in user_folder.iterdir()]
    return {"requests": files}
