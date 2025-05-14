from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import os
import base64
from io import BytesIO
import tempfile
from pathlib import Path
from weasyprint import HTML, CSS

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.resume import (
    PersonalInfo, ContactInfo, SocialMedia,
    Education, WorkExperience, Language, Skill,
    Certificate, Project
)

router = APIRouter(
    prefix="/pdf",
    tags=["pdf"]
)

templates = Jinja2Templates(directory="app/static")

@router.get("/generate")
async def generate_pdf(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a PDF resume from user data"""
    resume_data = await get_complete_resume_data(db, current_user)
    
    pdf_bytes = await generate_pdf_from_data(resume_data)
    
    filename = f"{current_user.phone_number}_resume.pdf" if current_user.phone_number else "resume.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

async def get_complete_resume_data(db: Session, user: User) -> Dict[str, Any]:
    """Fetch all resume data for a user"""
    personal_info = db.query(PersonalInfo).filter(PersonalInfo.user_id == user.id).first()
    contact_info = db.query(ContactInfo).filter(ContactInfo.user_id == user.id).first()
    social_media = db.query(SocialMedia).filter(SocialMedia.user_id == user.id).all()
    education = db.query(Education).filter(Education.user_id == user.id).all()
    work_experience = db.query(WorkExperience).filter(WorkExperience.user_id == user.id).all()
    languages = db.query(Language).filter(Language.user_id == user.id).all()
    skills = db.query(Skill).filter(Skill.user_id == user.id).all()
    certificates = db.query(Certificate).filter(Certificate.user_id == user.id).all()
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    
    return {
        "personal_info": personal_info,
        "contact_info": contact_info,
        "social_media": social_media,
        "education": education,
        "work_experience": work_experience,
        "languages": languages,
        "skills": skills,
        "certificates": certificates,
        "projects": projects,
        "user": user
    }

async def generate_pdf_from_data(resume_data: Dict[str, Any]) -> bytes:
    """Generate PDF from resume data using WeasyPrint"""
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("app/static"))
    template = env.get_template("resume_template.html")

    user = resume_data.get("user")
    if user and user.profile_picture:
        if user.profile_picture.startswith("/static/"):
            profile_pic_path = f"app{user.profile_picture}"
            if os.path.exists(profile_pic_path):
                user.profile_picture = f"file:///{os.path.abspath(profile_pic_path).replace(os.sep, '/')}"

    html_content = template.render(**resume_data)
    
    html = HTML(string=html_content)
    custom_css = """
    @page { margin: 0.5cm; }
    @font-face {
        font-family: 'Vazir';
        src: url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/Vazir.woff2') format('woff2');
        font-weight: normal;
        font-style: normal;
    }
    body {
        direction: rtl;
        text-align: right;
        font-family: 'Vazir', 'Tahoma', 'Arial', sans-serif;
    }
    .profile-picture-placeholder {
        color: white !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    .skills-list {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 15px;
        justify-content: flex-start;
        width: 100%;
    }
    .skill {
        background-color: #e8f4fc;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 14px;
        color: #2980b9;
        border: 1px solid #bde0f3;
        display: inline-block;
        white-space: nowrap;
        margin: 5px;
        flex: 0 0 auto;
        box-sizing: border-box;
    }
    """
    css = CSS(string=custom_css)
    pdf_bytes = html.write_pdf(stylesheets=[css])
    
    return pdf_bytes