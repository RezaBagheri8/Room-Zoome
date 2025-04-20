from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import create_access_token, Token
from app.db.session import get_db
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class PhoneNumberRequest(BaseModel):
    phone_number: str

class OTPVerifyRequest(BaseModel):
    phone_number: str
    otp_code: str

@router.post("/request-otp", response_model=dict)
def request_otp(request: PhoneNumberRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if not user:
        user = User(phone_number=request.phone_number)
        db.add(user)
    
    otp = user.generate_otp()
    db.commit()
    
    return {"message": "OTP sent successfully", "otp": otp}

@router.post("/verify-otp", response_model=Token)
def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.verify_otp(request.otp_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    user.is_verified = True
    db.commit()
    
    access_token = create_access_token(
        data={"sub": user.id}
    )
    return Token(access_token=access_token, token_type="bearer")