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
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.resume import (
    PersonalInfo, ContactInfo, SocialMedia,
    Education, WorkExperience, Language, Skill,
    Certificate, Project
)
from app.repositories.template import TemplateRepository

router = APIRouter(
    prefix="/pdf",
    tags=["pdf"]
)

templates = Jinja2Templates(directory="app/static")
template_repo = TemplateRepository()

@router.get("/generate")
async def generate_pdf(
    request: Request,
    template_id: int = None,
    template_name: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a PDF resume from user data using dynamic templates"""
    resume_data = await get_complete_resume_data(db, current_user)
    
    # Get template from database
    template_obj = None
    if template_id:
        template_obj = template_repo.get(db, template_id)
    elif template_name:
        template_obj = template_repo.get_by_name(db, template_name)
    else:
        # Default to first enabled template if none specified
        enabled_templates = template_repo.get_enabled_templates(db, limit=1)
        if enabled_templates:
            template_obj = enabled_templates[0]
    
    if not template_obj:
        raise HTTPException(
            status_code=404,
            detail="Template not found or disabled"
        )
    
    if not template_obj.is_enabled:
        raise HTTPException(
            status_code=400,
            detail="Template is disabled"
        )
    
    # Check if template is free or user has purchased access
    if not template_obj.is_free:
        has_access = template_repo.user_has_access(db, current_user.id, template_obj.id)
        if not has_access:
            raise HTTPException(status_code=400, detail="Access denied: template not purchased")
    
    pdf_bytes = await generate_pdf_from_data(resume_data, template_obj.template_path)
    
    filename = f"{current_user.phone_number}_resume.pdf" if current_user.phone_number else "resume.pdf"
    
    # Send email with PDF attachment if user has contact info with email
    if resume_data.get("contact_info") and resume_data["contact_info"].email:
        await send_resume_email(resume_data["contact_info"].email, pdf_bytes, filename)
    
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

async def generate_pdf_from_data(resume_data: Dict[str, Any], template_path: str) -> bytes:
    """Generate PDF from resume data using WeasyPrint"""
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("app/static"))
    
    # Use the provided template path
    template = env.get_template(template_path)
    
    user = resume_data.get("user")
    
    if user and user.profile_picture:
        if user.profile_picture.startswith("/static/"):
            profile_pic_path = f"app{user.profile_picture}"
            if os.path.exists(profile_pic_path):
                user.profile_picture = f"file:///{os.path.abspath(profile_pic_path).replace(os.sep, '/')}"

    html_content = template.render(**resume_data)
    
    html = HTML(string=html_content)
    
    # Determine if we're using RTL or LTR template based on template path
    is_rtl = "rtl" in template_path.lower() or "persian" in template_path.lower()
    
    # Base CSS that applies to all templates
    base_css = """
    @page { margin: 0.5cm; }
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
    
    # RTL specific CSS (Persian)
    rtl_css = """
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
    """
    
    # LTR specific CSS (English)
    ltr_css = """
    @font-face {
        font-family: 'Roboto';
        src: url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');
        font-weight: normal;
        font-style: normal;
    }
    body {
        direction: ltr;
        text-align: left;
        font-family: 'Roboto', 'Arial', sans-serif;
    }
    """
    
    # Combine the appropriate CSS based on template
    custom_css = base_css + (rtl_css if is_rtl else ltr_css)
    
    css = CSS(string=custom_css)
    pdf_bytes = html.write_pdf(stylesheets=[css])
    
    return pdf_bytes

async def send_resume_email(recipient_email: str, pdf_bytes: bytes, filename: str):
    """Send email with PDF resume attachment"""
    # Email configuration
    sender_email = "rezabagheri3831@gmail.com"
    sender_password = "vfli aoub rvhr scla"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # Changed to 465 for SSL

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Your Resume PDF"

    # Add body
    body = "Please find your resume PDF attached."
    message.attach(MIMEText(body, "plain"))

    # Add PDF attachment
    pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    pdf_attachment.add_header("Content-Disposition", "attachment", filename=filename)
    message.attach(pdf_attachment)

    # Send email
    try:
        async with aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port, use_tls=True, username=sender_email, password=sender_password) as smtp:
            await smtp.send_message(message)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        # Don't raise an exception to allow the PDF download to continue even if email fails