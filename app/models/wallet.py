from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class WalletChargeStatus:
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class WalletCharge(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    receipt_path = Column(String(255), nullable=False)
    time = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(
        Enum(WalletChargeStatus.PENDING, WalletChargeStatus.ACCEPTED, WalletChargeStatus.REJECTED, name="wallet_charge_status"),
        default=WalletChargeStatus.PENDING,
        nullable=False,
    )

    user = relationship("User", back_populates="wallet_charges")


