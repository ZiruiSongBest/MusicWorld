from fastapi import APIRouter, Request, UploadFile, File, Form
from pathlib import Path

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
    pass

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
