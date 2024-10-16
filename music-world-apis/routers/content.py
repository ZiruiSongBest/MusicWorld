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
    
    if not user_id:
        return {"error": "user_id cookie is missing"}

    user_folder = UPLOAD_DIR / user_id
    user_folder.mkdir(parents=True, exist_ok=True)

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

    if audio_path:
        audio_information = audio_analyzer_service.audio_analysis(audio_path, text_prompt)
    
    input_information = ""
    if text_prompt:
        input_information += (
            "User's text prompt: {text}\n".format(text=text_prompt)
        )
    if audio_path and audio_information[0] == 0:
        input_information += (
            "Audio: the user uploaded a audio piece with these analysis results: {audio_information}\n".format(audio_information=audio_information[1])
            )
    if image_path:
        input_information += (
            "Image: the user uploaded a image with this description: {image_information}\n".format(image_information=image_information)
        )
    if video_path:
        input_information += (
            "Video: the user uploaded a video with this description: {video_information}\n".format(video_information=video_information)
        )
    
    print('*' * 10)
    print('final prompt:', input_information)
    print('*' * 10)
        
    result_code, description = prompt_service.create_prompt(
        text=input_information,
    )

    print('-' * 10)
    print('final prompt:', description)
    print('-' * 10)

    generated_audio_path = user_folder / "generated_audio.wav"

    # generate audio
    generated_audio = audio_generator_service.generate_audio(
        description
    )
    audio_generator_service.save_audio(generated_audio, generated_audio_path)

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
        # "audio_url": audio_url,
    # }


@router.get("/requests")
async def list_user_requests(request: Request):
    user_id = request.cookies.get("user_id")
    user_folder = UPLOAD_DIR / user_id
    if not user_folder.exists():
        return {"requests": []}
    files = [str(file) for file in user_folder.iterdir()]
    return {"requests": files}
