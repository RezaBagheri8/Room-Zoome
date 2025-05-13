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

# Create templates object
templates = Jinja2Templates(directory="app/static")

@router.get("/generate")
async def generate_pdf(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a PDF resume from user data"""
    # Fetch all resume data for the current user
    resume_data = await get_complete_resume_data(db, current_user)
    
    # Generate PDF directly from resume data using ReportLab
    pdf_bytes = await generate_pdf_from_data(resume_data)
    
    # Return the PDF as a downloadable file
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
    # Create a Jinja2 environment to render the template
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("app/static"))
    template = env.get_template("resume_template.html")

    # Process profile picture URL to ensure it works in PDF
    user = resume_data.get("user")
    if user and user.profile_picture:
        # Convert relative URL to absolute file path for WeasyPrint
        if user.profile_picture.startswith("/static/"):
            # Get the absolute path to the file
            profile_pic_path = f"app{user.profile_picture}"
            # Make sure the URL in the template points to a file that exists
            if os.path.exists(profile_pic_path):
                # For WeasyPrint, we need to use file:// protocol for local files
                user.profile_picture = f"file:///{os.path.abspath(profile_pic_path).replace(os.sep, '/')}"

    # Render the HTML template with the resume data
    html_content = template.render(**resume_data)
    
    # Use WeasyPrint to generate PDF with custom styling
    html = HTML(string=html_content)
    # Add custom CSS for better PDF rendering
    custom_css = """
    @page { margin: 0.5cm; }
    @font-face {
        font-family: 'Roboto';
        src: local('Roboto'), local('Segoe UI'), local('Arial');
    }
    .profile-picture-placeholder {
        color: white !important;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    """
    css = CSS(string=custom_css)
    pdf_bytes = html.write_pdf(stylesheets=[css])
    
    return pdf_bytes