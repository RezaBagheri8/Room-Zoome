from datetime import date
from pathlib import Path
import os
import shutil
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

UPLOAD_DIR = Path("app/static/uploads/profile_pictures")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def save_upload_file(upload_file: UploadFile, user_id: int) -> str:
    """Save the uploaded file and return the file path"""
    file_extension = os.path.splitext(upload_file.filename)[1]
    filename = f"profile_{user_id}{file_extension}"
    file_path = UPLOAD_DIR / filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return f"/static/uploads/profile_pictures/{filename}"

@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    birth_date: Optional[date] = Form(None),
    profile_picture: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if first_name is not None:
        current_user.first_name = first_name
    if last_name is not None:
        current_user.last_name = last_name
    if birth_date is not None:
        current_user.birth_date = birth_date
    
    if profile_picture:
        file_path = await save_upload_file(profile_picture, current_user.id)
        current_user.profile_picture = file_path
    
    db.commit()
    db.refresh(current_user)
    
    return current_user