from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.resume import (
    PersonalInfo, ContactInfo, SocialMedia,
    Education, WorkExperience, Language, Skill,
    Certificate, Project
)
from app.schemas.resume import (
    PersonalInfoCreate, ContactInfoCreate, SocialMediaCreate,
    EducationCreate, WorkExperienceCreate, LanguageCreate, SkillCreate,
    CertificateCreate, ProjectCreate,
    PersonalInfoResponse, ContactInfoResponse, SocialMediaResponse,
    EducationResponse, WorkExperienceResponse, LanguageResponse, SkillResponse,
    CertificateResponse, ProjectResponse
)

router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)

# Tab 1: Personal Info, Contact Info, Social Media
@router.put("/personal-info", response_model=PersonalInfoResponse)
def update_personal_info(
    personal_info: PersonalInfoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update or create personal information for the current user"""
    db_personal_info = db.query(PersonalInfo).filter(PersonalInfo.user_id == current_user.id).first()
    
    if db_personal_info:
        # Update existing record
        for key, value in personal_info.dict(exclude_unset=True).items():
            setattr(db_personal_info, key, value)
    else:
        # Create new record
        db_personal_info = PersonalInfo(**personal_info.dict(), user_id=current_user.id)
        db.add(db_personal_info)
    
    db.commit()
    db.refresh(db_personal_info)
    return db_personal_info

@router.get("/personal-info", response_model=PersonalInfoResponse)
def get_personal_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get personal information for the current user"""
    db_personal_info = db.query(PersonalInfo).filter(PersonalInfo.user_id == current_user.id).first()
    if not db_personal_info:
        raise HTTPException(status_code=404, detail="Personal information not found")
    return db_personal_info

@router.put("/contact-info", response_model=ContactInfoResponse)
def update_contact_info(
    contact_info: ContactInfoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update or create contact information for the current user"""
    db_contact_info = db.query(ContactInfo).filter(ContactInfo.user_id == current_user.id).first()
    
    if db_contact_info:
        # Update existing record
        for key, value in contact_info.dict(exclude_unset=True).items():
            setattr(db_contact_info, key, value)
    else:
        # Create new record
        db_contact_info = ContactInfo(**contact_info.dict(), user_id=current_user.id)
        db.add(db_contact_info)
    
    db.commit()
    db.refresh(db_contact_info)
    return db_contact_info

@router.get("/contact-info", response_model=ContactInfoResponse)
def get_contact_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contact information for the current user"""
    db_contact_info = db.query(ContactInfo).filter(ContactInfo.user_id == current_user.id).first()
    if not db_contact_info:
        raise HTTPException(status_code=404, detail="Contact information not found")
    return db_contact_info

@router.post("/social-media", response_model=SocialMediaResponse)
def create_social_media(
    social_media: SocialMediaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new social media profile for the current user"""
    db_social_media = SocialMedia(**social_media.dict(), user_id=current_user.id)
    db.add(db_social_media)
    db.commit()
    db.refresh(db_social_media)
    return db_social_media

@router.put("/social-media/{social_media_id}", response_model=SocialMediaResponse)
def update_social_media(
    social_media_id: int,
    social_media: SocialMediaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing social media profile"""
    db_social_media = db.query(SocialMedia).filter(
        SocialMedia.id == social_media_id,
        SocialMedia.user_id == current_user.id
    ).first()
    
    if not db_social_media:
        raise HTTPException(status_code=404, detail="Social media profile not found")
    
    for key, value in social_media.dict().items():
        setattr(db_social_media, key, value)
    
    db.commit()
    db.refresh(db_social_media)
    return db_social_media

@router.delete("/social-media/{social_media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_social_media(
    social_media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a social media profile"""
    db_social_media = db.query(SocialMedia).filter(
        SocialMedia.id == social_media_id,
        SocialMedia.user_id == current_user.id
    ).first()
    
    if not db_social_media:
        raise HTTPException(status_code=404, detail="Social media profile not found")
    
    db.delete(db_social_media)
    db.commit()
    return {"status": "success"}

@router.get("/social-media", response_model=List[SocialMediaResponse])
def get_social_media(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all social media profiles for the current user"""
    return db.query(SocialMedia).filter(SocialMedia.user_id == current_user.id).all()

# Tab 2: Education History
@router.post("/education", response_model=EducationResponse)
def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new education entry for the current user"""
    db_education = Education(**education.dict(), user_id=current_user.id)
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education

@router.put("/education/{education_id}", response_model=EducationResponse)
def update_education(
    education_id: int,
    education: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing education entry"""
    db_education = db.query(Education).filter(
        Education.id == education_id,
        Education.user_id == current_user.id
    ).first()
    
    if not db_education:
        raise HTTPException(status_code=404, detail="Education entry not found")
    
    for key, value in education.dict().items():
        setattr(db_education, key, value)
    
    db.commit()
    db.refresh(db_education)
    return db_education

@router.delete("/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an education entry"""
    db_education = db.query(Education).filter(
        Education.id == education_id,
        Education.user_id == current_user.id
    ).first()
    
    if not db_education:
        raise HTTPException(status_code=404, detail="Education entry not found")
    
    db.delete(db_education)
    db.commit()
    return {"status": "success"}

@router.get("/education", response_model=List[EducationResponse])
def get_education(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all education entries for the current user"""
    return db.query(Education).filter(Education.user_id == current_user.id).all()

# Tab 3: Work Experience
@router.post("/work-experience", response_model=WorkExperienceResponse)
def create_work_experience(
    work_experience: WorkExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new work experience entry for the current user"""
    db_work_experience = WorkExperience(**work_experience.dict(), user_id=current_user.id)
    db.add(db_work_experience)
    db.commit()
    db.refresh(db_work_experience)
    return db_work_experience

@router.put("/work-experience/{work_experience_id}", response_model=WorkExperienceResponse)
def update_work_experience(
    work_experience_id: int,
    work_experience: WorkExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing work experience entry"""
    db_work_experience = db.query(WorkExperience).filter(
        WorkExperience.id == work_experience_id,
        WorkExperience.user_id == current_user.id
    ).first()
    
    if not db_work_experience:
        raise HTTPException(status_code=404, detail="Work experience entry not found")
    
    for key, value in work_experience.dict().items():
        setattr(db_work_experience, key, value)
    
    db.commit()
    db.refresh(db_work_experience)
    return db_work_experience

@router.delete("/work-experience/{work_experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_experience(
    work_experience_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a work experience entry"""
    db_work_experience = db.query(WorkExperience).filter(
        WorkExperience.id == work_experience_id,
        WorkExperience.user_id == current_user.id
    ).first()
    
    if not db_work_experience:
        raise HTTPException(status_code=404, detail="Work experience entry not found")
    
    db.delete(db_work_experience)
    db.commit()
    return {"status": "success"}

@router.get("/work-experience", response_model=List[WorkExperienceResponse])
def get_work_experience(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all work experience entries for the current user"""
    return db.query(WorkExperience).filter(WorkExperience.user_id == current_user.id).all()

# Tab 4: Languages, Skills, Certificates
@router.post("/language", response_model=LanguageResponse)
def create_language(
    language: LanguageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new language for the current user"""
    db_language = Language(**language.dict(), user_id=current_user.id)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language

@router.put("/language/{language_id}", response_model=LanguageResponse)
def update_language(
    language_id: int,
    language: LanguageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing language"""
    db_language = db.query(Language).filter(
        Language.id == language_id,
        Language.user_id == current_user.id
    ).first()
    
    if not db_language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    for key, value in language.dict().items():
        setattr(db_language, key, value)
    
    db.commit()
    db.refresh(db_language)
    return db_language

@router.delete("/language/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_language(
    language_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a language"""
    db_language = db.query(Language).filter(
        Language.id == language_id,
        Language.user_id == current_user.id
    ).first()
    
    if not db_language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    db.delete(db_language)
    db.commit()
    return {"status": "success"}

@router.get("/language", response_model=List[LanguageResponse])
def get_languages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all languages for the current user"""
    return db.query(Language).filter(Language.user_id == current_user.id).all()

@router.post("/skill", response_model=SkillResponse)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new skill for the current user"""
    db_skill = Skill(**skill.dict(), user_id=current_user.id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.put("/skill/{skill_id}", response_model=SkillResponse)
def update_skill(
    skill_id: int,
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing skill"""
    db_skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == current_user.id
    ).first()
    
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in skill.dict().items():
        setattr(db_skill, key, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.delete("/skill/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a skill"""
    db_skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == current_user.id
    ).first()
    
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(db_skill)
    db.commit()
    return {"status": "success"}

@router.get("/skill", response_model=List[SkillResponse])
def get_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all skills for the current user"""
    return db.query(Skill).filter(Skill.user_id == current_user.id).all()

@router.post("/certificate", response_model=CertificateResponse)
def create_certificate(
    certificate: CertificateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new certificate for the current user"""
    db_certificate = Certificate(**certificate.dict(), user_id=current_user.id)
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

@router.put("/certificate/{certificate_id}", response_model=CertificateResponse)
def update_certificate(
    certificate_id: int,
    certificate: CertificateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing certificate"""
    db_certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id,
        Certificate.user_id == current_user.id
    ).first()
    
    if not db_certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    for key, value in certificate.dict().items():
        setattr(db_certificate, key, value)
    
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

@router.delete("/certificate/{certificate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a certificate"""
    db_certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id,
        Certificate.user_id == current_user.id
    ).first()
    
    if not db_certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    db.delete(db_certificate)
    db.commit()
    return {"status": "success"}

@router.get("/certificate", response_model=List[CertificateResponse])
def get_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all certificates for the current user"""
    return db.query(Certificate).filter(Certificate.user_id == current_user.id).all()

# Tab 5: Projects
@router.post("/project", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new project for the current user"""
    db_project = Project(**project.dict(), user_id=current_user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.put("/project/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing project"""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/project/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a project"""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return {"status": "success"}

@router.get("/project", response_model=List[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all projects for the current user"""
    return db.query(Project).filter(Project.user_id == current_user.id).all()