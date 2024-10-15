from fastapi import Request, Response
import uuid

async def add_user_id_cookie(request: Request, call_next):
    user_id = request.cookies.get("user_id")

    response = await call_next(request)

    if not user_id:
        user_id = str(uuid.uuid4())
        response.set_cookie(key="user_id", value=user_id, httponly=True, max_age=86400)  # 24 hours expiry
    
    return response
