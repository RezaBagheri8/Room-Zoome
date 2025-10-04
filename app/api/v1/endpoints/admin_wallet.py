from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.wallet import WalletChargeStatus, WalletCharge
from app.repositories.wallet import WalletChargeRepository
from app.schemas.wallet import WalletChargeResponse


router = APIRouter(prefix="/admin/wallet", tags=["admin-wallet"])

wallet_repo = WalletChargeRepository()


def check_admin_permissions(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/charges", response_model=List[WalletChargeResponse])
def list_wallet_charges(
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions),
):
    query = db.query(WalletCharge)
    if status:
        query = query.filter(WalletCharge.status == status)
    return query.order_by(WalletCharge.id.desc()).offset(skip).limit(limit).all()


@router.get("/charges/{charge_id}", response_model=WalletChargeResponse)
def get_wallet_charge(
    charge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions),
):
    charge = wallet_repo.get(db, charge_id)
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    return charge


@router.post("/charges/{charge_id}/accept", response_model=WalletChargeResponse)
def accept_wallet_charge(
    charge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions),
):
    charge = wallet_repo.get(db, charge_id)
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    if charge.status != WalletChargeStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending charges can be accepted")

    user = db.query(User).filter(User.id == charge.user_id).with_for_update().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        charge.status = WalletChargeStatus.ACCEPTED
        user.wallet_balance = float(user.wallet_balance or 0.0) + float(charge.amount)
        db.add(user)
        db.add(charge)
        db.commit()
        db.refresh(charge)
    except Exception:
        db.rollback()
        raise
    return charge


@router.post("/charges/{charge_id}/reject", response_model=WalletChargeResponse)
def reject_wallet_charge(
    charge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions),
):
    charge = wallet_repo.get(db, charge_id)
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    if charge.status != WalletChargeStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending charges can be rejected")

    charge.status = WalletChargeStatus.REJECTED
    db.add(charge)
    db.commit()
    db.refresh(charge)
    return charge


