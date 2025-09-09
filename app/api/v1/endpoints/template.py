from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.repositories.template import TemplateRepository
from app.schemas.template import TemplateListResponse

router = APIRouter(
    prefix="/template",
    tags=["template"]
)

template_repo = TemplateRepository()


@router.get("/options", response_model=List[TemplateListResponse])
async def get_all_templates(
    db: Session = Depends(get_db)
):
    """Get all templates with comprehensive data"""
    try:
        templates = template_repo.get_all_templates(db)
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching templates: {str(e)}")