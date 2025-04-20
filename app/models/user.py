from sqlalchemy import Column, String, Boolean, Integer, DateTime, Date
from app.models.base import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    profile_picture = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    is_verified = Column(Boolean, default=False)
    otp_code = Column(String(6), nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)
    
    # Resume relationships
    personal_info = relationship("PersonalInfo", back_populates="user", uselist=False)
    contact_info = relationship("ContactInfo", back_populates="user", uselist=False)
    social_media = relationship("SocialMedia", back_populates="user")
    education = relationship("Education", back_populates="user")
    work_experiences = relationship("WorkExperience", back_populates="user")
    languages = relationship("Language", back_populates="user")
    skills = relationship("Skill", back_populates="user")
    certificates = relationship("Certificate", back_populates="user")
    projects = relationship("Project", back_populates="user")
    
    def generate_otp(self):
        import random
        self.otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
        return self.otp_code
    
    def verify_otp(self, otp: str) -> bool:
        if not self.otp_code or not self.otp_expires_at:
            return False
        if datetime.utcnow() > self.otp_expires_at:
            return False
        return self.otp_code == otp