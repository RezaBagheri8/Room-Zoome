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
from fastapi import HTTPException
from app.models import resume as resume_models
from app.schemas.user import UserProfileResponse, UserResponse
from app.schemas.resume import ResumeResponse

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

@router.put("/profile", response_model=UserResponse)
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


@router.get("/profile/{user_id}", response_model=UserProfileResponse, tags=["users"])
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch resume data
    personal_info = db.query(resume_models.PersonalInfo).filter(resume_models.PersonalInfo.user_id == user_id).first()
    contact_info = db.query(resume_models.ContactInfo).filter(resume_models.ContactInfo.user_id == user_id).first()
    social_media = db.query(resume_models.SocialMedia).filter(resume_models.SocialMedia.user_id == user_id).all()
    education = db.query(resume_models.Education).filter(resume_models.Education.user_id == user_id).all()
    work_experiences = db.query(resume_models.WorkExperience).filter(resume_models.WorkExperience.user_id == user_id).all()
    languages = db.query(resume_models.Language).filter(resume_models.Language.user_id == user_id).all()
    skills = db.query(resume_models.Skill).filter(resume_models.Skill.user_id == user_id).all()
    certificates = db.query(resume_models.Certificate).filter(resume_models.Certificate.user_id == user_id).all()
    projects = db.query(resume_models.Project).filter(resume_models.Project.user_id == user_id).all()

    resume = ResumeResponse(
        personal_info=personal_info,
        contact_info=contact_info,
        social_media=social_media,
        education=education,
        work_experiences=work_experiences,
        languages=languages,
        skills=skills,
        certificates=certificates,
        projects=projects
    )

    return UserProfileResponse(user=user, resume=resume)

@router.get("/me", response_model=UserResponse, tags=["users"])
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user