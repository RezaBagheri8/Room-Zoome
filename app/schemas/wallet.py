from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WalletChargeBase(BaseModel):
    amount: float = Field(..., gt=0)


class WalletChargeCreate(WalletChargeBase):
    pass


class WalletChargeUpdateStatus(BaseModel):
    status: str


class WalletChargeResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    receipt_path: str
    time: datetime
    status: str

    class Config:
        from_attributes = True


