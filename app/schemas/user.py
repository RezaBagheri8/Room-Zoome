from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class UserResponse(BaseModel):
    id: int
    phone_number: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture: Optional[str] = None
    birth_date: Optional[date] = None
    is_verified: bool
    otp_code: Optional[str] = None
    otp_expires_at: Optional[datetime] = None
    wallet_balance: float

    class Config:
        from_attributes = True

from app.schemas.resume import ResumeResponse

class UserProfileResponse(BaseModel):
    user: UserResponse
    resume: ResumeResponse

    class Config:
        from_attributes = True