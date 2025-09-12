from typing import List, Optional

from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.models.wallet import WalletCharge, WalletChargeStatus
from app.schemas.wallet import WalletChargeCreate


class WalletChargeRepository(BaseRepository[WalletCharge, WalletChargeCreate, dict]):
    def __init__(self):
        super().__init__(WalletCharge)

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[WalletCharge]:
        return (
            db.query(WalletCharge)
            .filter(WalletCharge.user_id == user_id)
            .order_by(WalletCharge.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_status(self, db: Session, charge: WalletCharge, status: str) -> WalletCharge:
        charge.status = status
        db.add(charge)
        db.commit()
        db.refresh(charge)
        return charge


