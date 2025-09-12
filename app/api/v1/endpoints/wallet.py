from pathlib import Path
import os
import shutil
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.wallet import WalletChargeStatus
from app.repositories.wallet import WalletChargeRepository
from app.schemas.wallet import WalletChargeCreate, WalletChargeResponse


router = APIRouter(prefix="/wallet", tags=["wallet"])

wallet_repo = WalletChargeRepository()

UPLOAD_DIR = Path("app/static/uploads/wallet_receipts")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_receipt(upload_file: UploadFile, user_id: int) -> str:
    file_extension = os.path.splitext(upload_file.filename)[1]
    filename = f"receipt_{user_id}_{upload_file.filename}"
    safe_filename = filename.replace(" ", "_")
    file_path = UPLOAD_DIR / safe_filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return f"uploads/wallet_receipts/{safe_filename}"


@router.get("/balance", response_model=float)
def get_wallet_balance(current_user: User = Depends(get_current_user)):
    return float(current_user.wallet_balance or 0.0)


@router.post("/charges", response_model=WalletChargeResponse)
async def create_wallet_charge(
    amount: float = Form(..., gt=0),
    receipt: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    receipt_path = await save_receipt(receipt, current_user.id)
    charge_in = WalletChargeCreate(amount=amount)
    charge = wallet_repo.create(
        db,
        obj_in={
            "user_id": current_user.id,
            "amount": amount,
            "receipt_path": receipt_path,
            "status": WalletChargeStatus.PENDING,
        },
    )
    return charge


@router.get("/charges", response_model=List[WalletChargeResponse])
def list_my_wallet_charges(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return wallet_repo.get_by_user(db, current_user.id, skip=skip, limit=limit)


