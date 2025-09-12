from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import hashlib

from app.db.session import get_db
from app.models.admin import Admin
from app.core.security import create_access_token, Token


router = APIRouter(prefix="/admin", tags=["auth"])


class AdminLoginRequest(BaseModel):
    username: str
    password: str


def _hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


@router.post("/login", response_model=Token)
def admin_login(payload: AdminLoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == payload.username).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if admin.password_hash != _hash_password(payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": f"admin:{admin.id}", "role": "admin"})
    return Token(access_token=access_token, token_type="bearer")


