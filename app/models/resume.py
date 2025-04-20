from sqlalchemy import Column, String, Boolean, Integer, Date, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

# Enum for gender options
class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

# Enum for military service status
class MilitaryServiceStatus(str, enum.Enum):
    COMPLETED = "completed"
    EXEMPTED = "exempted"
    ONGOING = "ongoing"
    NOT_APPLICABLE = "not_applicable"

# Enum for proficiency levels
class ProficiencyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    NATIVE = "native"

class PersonalInfo(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    gender = Column(Enum(Gender), nullable=True)
    is_married = Column(Boolean, nullable=True)
    military_service_status = Column(Enum(MilitaryServiceStatus), nullable=True)
    about_me = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="personal_info")

class ContactInfo(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    phone_number = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    landline = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="contact_info")

class SocialMedia(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(50), nullable=False)
    profile_id = Column(String(100), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="social_media")

class Education(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    degree = Column(String(100), nullable=False)
    major = Column(String(100), nullable=False)
    university_type = Column(String(100), nullable=True)
    university_name = Column(String(255), nullable=False)
    grade = Column(String(20), nullable=True)
    entrance_year = Column(Integer, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    country = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    is_current = Column(Boolean, default=False)
    
    # Relationship
    user = relationship("User", back_populates="education")

class WorkExperience(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    position = Column(String(100), nullable=False)
    company_name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=True)
    province = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="work_experiences")

class Language(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(50), nullable=False)
    proficiency = Column(Enum(ProficiencyLevel), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="languages")

class Skill(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(100), nullable=False)
    proficiency = Column(Enum(ProficiencyLevel), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="skills")

class Certificate(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    institute = Column(String(255), nullable=False)
    date = Column(Date, nullable=True)
    link = Column(String(255), nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="certificates")

class Project(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    customer_name = Column(String(255), nullable=True)
    date = Column(Date, nullable=True)
    link = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="projects")