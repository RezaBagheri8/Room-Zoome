from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    direction: str = Field(default="ltr", regex="^(ltr|rtl)$")
    language: str = Field(default="English", max_length=50)
    price: float = Field(default=0.0, ge=0.0)
    is_free: bool = Field(default=True)
    is_enabled: bool = Field(default=True)
    template_path: str = Field(..., min_length=1, max_length=255)
    preview_path: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=50)
    sort_order: int = Field(default=0, ge=0)


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    direction: Optional[str] = Field(None, regex="^(ltr|rtl)$")
    language: Optional[str] = Field(None, max_length=50)
    price: Optional[float] = Field(None, ge=0.0)
    is_free: Optional[bool] = None
    is_enabled: Optional[bool] = None
    template_path: Optional[str] = Field(None, min_length=1, max_length=255)
    preview_path: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=50)
    sort_order: Optional[int] = Field(None, ge=0)


class TemplateResponse(TemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TemplateListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    direction: str
    language: str
    price: float
    is_free: bool
    is_enabled: bool
    preview_path: Optional[str]
    category: Optional[str]
    sort_order: int

    class Config:
        from_attributes = True
