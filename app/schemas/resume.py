from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

# Enum definitions for validation
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class MilitaryServiceStatus(str, Enum):
    COMPLETED = "completed"
    EXEMPTED = "exempted"
    ONGOING = "ongoing"
    NOT_APPLICABLE = "not_applicable"

class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    NATIVE = "native"

# Base schemas with shared configurations
class ResumeBaseSchema(BaseModel):
    class Config:
        from_attributes = True

# Request schemas (for creating/updating)
class PersonalInfoCreate(BaseModel):
    gender: Optional[Gender] = None
    is_married: Optional[bool] = None
    military_service_status: Optional[MilitaryServiceStatus] = None
    about_me: Optional[str] = None

class ContactInfoCreate(BaseModel):
    phone_number: Optional[str] = Field(None, max_length=15)
    email: Optional[str] = Field(None, max_length=100)
    landline: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)
    country: Optional[str] = Field(None, max_length=100)
    province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None

class SocialMediaCreate(BaseModel):
    name: str = Field(..., max_length=50)
    profile_id: str = Field(..., max_length=100)

class EducationCreate(BaseModel):
    degree: str = Field(..., max_length=100)
    major: str = Field(..., max_length=100)
    university_type: Optional[str] = Field(None, max_length=100)
    university_name: str = Field(..., max_length=255)
    grade: Optional[str] = Field(None, max_length=20)
    entrance_year: Optional[int] = None
    graduation_year: Optional[int] = None
    country: Optional[str] = Field(None, max_length=100)
    province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    is_current: Optional[bool] = False

class WorkExperienceCreate(BaseModel):
    position: str = Field(..., max_length=100)
    company_name: str = Field(..., max_length=255)
    country: Optional[str] = Field(None, max_length=100)
    province: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    start_date: date
    end_date: Optional[date] = None
    is_current: Optional[bool] = False
    description: Optional[str] = None

class LanguageCreate(BaseModel):
    name: str = Field(..., max_length=50)
    proficiency: ProficiencyLevel

class SkillCreate(BaseModel):
    name: str = Field(..., max_length=100)
    proficiency: ProficiencyLevel

class CertificateCreate(BaseModel):
    title: str = Field(..., max_length=255)
    institute: str = Field(..., max_length=255)
    date: Optional[date] = None
    link: Optional[str] = Field(None, max_length=255)

class ProjectCreate(BaseModel):
    title: str = Field(..., max_length=255)
    customer_name: Optional[str] = Field(None, max_length=255)
    date: Optional[date] = None
    link: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None

# Response schemas (for returning data)
class PersonalInfoResponse(PersonalInfoCreate, ResumeBaseSchema):
    id: int
    user_id: int

class ContactInfoResponse(ContactInfoCreate, ResumeBaseSchema):
    id: int
    user_id: int

class SocialMediaResponse(SocialMediaCreate, ResumeBaseSchema):
    id: int
    user_id: int

class EducationResponse(EducationCreate, ResumeBaseSchema):
    id: int
    user_id: int

class WorkExperienceResponse(WorkExperienceCreate, ResumeBaseSchema):
    id: int
    user_id: int

class LanguageResponse(LanguageCreate, ResumeBaseSchema):
    id: int
    user_id: int

class SkillResponse(SkillCreate, ResumeBaseSchema):
    id: int
    user_id: int

class CertificateResponse(CertificateCreate, ResumeBaseSchema):
    id: int
    user_id: int

class ProjectResponse(ProjectCreate, ResumeBaseSchema):
    id: int
    user_id: int

# Complete resume response
class ResumeResponse(BaseModel):
    personal_info: Optional[PersonalInfoResponse] = None
    contact_info: Optional[ContactInfoResponse] = None
    social_media: List[SocialMediaResponse] = []
    education: List[EducationResponse] = []
    work_experiences: List[WorkExperienceResponse] = []
    languages: List[LanguageResponse] = []
    skills: List[SkillResponse] = []
    certificates: List[CertificateResponse] = []
    projects: List[ProjectResponse] = []
    
    class Config:
        from_attributes = True