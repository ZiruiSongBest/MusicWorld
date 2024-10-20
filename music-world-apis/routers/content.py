import json
from fastapi import APIRouter, Request, UploadFile, File, Form, Header
from services.AudioAnalyzerService import AudioAnalyzerService, audio_analyzer_service
from services.AudioGeneratorService import AudioGenerator, audio_generator_service
from services.PromptService import PromptService, prompt_service
from services.prompt import prompt_template
from utils.file_utils import save_multiple_files, schedule_deletion
from pathlib import Path
from typing import Optional
import asyncio
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.background import BackgroundTask
import uuid

router = APIRouter()

UPLOAD_DIR = Path("uploads")

class AudioStreamWithDescriptionResponse(StreamingResponse):
    def __init__(self, content, title, description, theme, *args, **kwargs):
        super().__init__(content, *args, **kwargs)
        self.title = self._sanitize_header_value(title)
        self.description = self._sanitize_header_value(description)
        self.theme = self._sanitize_header_value(theme)

    def _sanitize_header_value(self, value):
        # Replace newlines with spaces, limit the length, and remove any illegal characters
        sanitized_value = ' '.join(value.split())[:200]
        return sanitized_value.encode('ascii', 'ignore').decode('ascii')

    async def __call__(self, scope, receive, send):
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"application/octet-stream"),
                (b"x-audio-title", self.title.encode('utf-8')),
                (b"x-audio-description", self.description.encode('utf-8')),
                (b"x-audio-theme", self.theme.encode('utf-8')),
            ],
        })
        
        async for chunk in self.body_iterator:
            await send({
                "type": "http.response.body",
                "body": chunk,
                "more_body": True,
            })
        
        await send({
            "type": "http.response.body",
            "body": b"",
            "more_body": False,
        })

@router.post("/generate")
async def generate_content(
    request: Request,
    text_prompt: str = Form(None),
    text_files: list[UploadFile] = File(None),
    audio: list[UploadFile] = File(None),
    image: list[UploadFile] = File(None),
    video: list[UploadFile] = File(None),
    x_network_address: str = Header(None)
):
    print(f"Received network address: {x_network_address}")
    print(f"Received text prompt: {text_prompt}")
    print(f"Received text files: {len(text_files) if text_files else 0}")
    print(f"Received audio files: {len(audio) if audio else 0}")
    print(f"Received image files: {len(image) if image else 0}")
    print(f"Received video files: {len(video) if video else 0}")
    
    user_id = request.cookies.get("user_id")
    
    if not user_id:
        # Generate a temporary user ID if not provided
        user_id = str(uuid.uuid4())

    user_folder = UPLOAD_DIR / user_id
    user_folder.mkdir(parents=True, exist_ok=True)

    # Save text prompt to a file
    if text_prompt:
        prompt_file_path = user_folder / "text_prompt.txt"
        with open(prompt_file_path, "w") as f:
            f.write(text_prompt)
        asyncio.create_task(schedule_deletion(prompt_file_path))

    # Save uploaded files
    text_paths = await save_multiple_files(text_files, user_id) if text_files else []
    audio_paths = await save_multiple_files(audio, user_id) if audio else []
    image_paths = await save_multiple_files(image, user_id) if image else []
    video_paths = await save_multiple_files(video, user_id) if video else []

    # Schedule deletion after 24 hours
    for path in text_paths + audio_paths + image_paths + video_paths:
        asyncio.create_task(schedule_deletion(path))
        
    multi_modal_information = f"User's text prompt: {text_prompt}\n" if text_prompt else ""
        
    text_information = prompt_service.get_text(text_paths)
    # TODO: Get summarized content from text_information
    # multi_modal_information += (
    #     f"User's text file input: {text_information}\n"
    # )
    
    multi_modal_information += (
        f"User's audio file input: \n"
    ) if audio_paths else ""
    
    for i, audio_path in enumerate(audio_paths):
        audio_information = audio_analyzer_service.audio_analysis(audio_path, text_prompt)
        print(f'audio {i}: {audio_information}')
        multi_modal_information += (
            f"Audio piece {i}: {audio_information}\n"
        )
    
    # TODO: Get summarized content from video_information
    # for i, video_path in enumerate(video_paths):
        # video_information = prompt_service.get_response(video_path, text_prompt)
        # print(f'video {i}: {video_information}')
    
    # print("*" * 10)
    # print("multi_modal_information: ", multi_modal_information)
    # print("*" * 10)
    
    ### Generate audio prompt
    audio_prompt = prompt_service.create_prompt("generate_audio_prompt", multi_modal_information, image_paths=image_paths)
    result_code, theme = prompt_service.get_response(audio_prompt)
    
    # Generate title and description
    summarize_prompt = prompt_service.create_prompt("summarize", multi_modal_information)
    result_code, response = prompt_service.get_response(summarize_prompt, json_output=True)
    summary = prompt_service.parse_summary_response(response)
    title = summary.get("Title", "Untitled")
    description = summary.get("Description", "No description available")
        
    
    # print("description: ", description)

    generated_audio_path = user_folder / "generated_audio.wav"
    # generated_audio_path = "uploads/7d6617f5-7c75-4144-8859-dee3f6cb85d5/audio_1.mp3"

    # generate audio
    generated_audio = audio_generator_service.generate_audio(
        theme
    )
    audio_generator_service.save_audio(generated_audio, generated_audio_path)

    # with open(album_image_path, "wb") as f:
    #     f.write(album_image)

    # asyncio.create_task(schedule_deletion(generated_audio_path))
    # asyncio.create_task(schedule_deletion(album_image_path))

    # Convert the string path to a Path object
    generated_audio_path = Path(generated_audio_path)

    def iterfile():
        with open(generated_audio_path, mode="rb") as file_like:
            yield from file_like

    # title = "This is a test title"
    # description = "This is a test description"
    # theme = "This is a test theme"
    
    response = AudioStreamWithDescriptionResponse(
        content=iterfile(),
        media_type="audio/mpeg",
        title=title,
        description=description,
        theme=theme,
        background=BackgroundTask(generated_audio_path.unlink)
    )
    
    # Set the user_id cookie if it wasn't present in the request
    if not request.cookies.get("user_id"):
        response.set_cookie(key="user_id", value=user_id)
    
    return response

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
