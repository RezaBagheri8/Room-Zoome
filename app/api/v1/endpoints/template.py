from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.repositories.template import TemplateRepository
from app.schemas.template import TemplateListResponse, PurchaseTemplateRequest
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.user_template import UserTemplateRepository
from app.models.template import Template

router = APIRouter(
    prefix="/template",
    tags=["template"]
)

template_repo = TemplateRepository()
user_template_repo = UserTemplateRepository()


@router.get("/options", response_model=List[TemplateListResponse])
async def get_all_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all templates with purchased flag for the current user"""
    try:
        templates = template_repo.get_all_templates(db)
        purchased_links = user_template_repo.list_by_user(db, current_user.id)
        purchased_template_ids = {link.template_id for link in purchased_links}

        results: List[TemplateListResponse] = []
        for tpl in templates:
            results.append(
                TemplateListResponse(
                    id=tpl.id,
                    name=tpl.name,
                    description=tpl.description,
                    direction=tpl.direction,
                    language=tpl.language,
                    price=tpl.price,
                    is_free=tpl.is_free,
                    is_enabled=tpl.is_enabled,
                    preview_path=tpl.preview_path,
                    category=tpl.category,
                    sort_order=tpl.sort_order,
                    purchased=(tpl.id in purchased_template_ids) if not tpl.is_free else None,
                )
            )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching templates: {str(e)}")


@router.post("/purchase", response_model=TemplateListResponse)
async def purchase_template(
    payload: PurchaseTemplateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    template: Optional[Template] = template_repo.get(db, payload.template_id)
    if not template or not template.is_enabled:
        raise HTTPException(status_code=404, detail="Template not found")

    if template.is_free:
        # Free templates are available without recording a purchase
        return template

    if user_template_repo.get_by_user_and_template(db, current_user.id, template.id):
        raise HTTPException(status_code=400, detail="Template already purchased")

    user = db.query(User).filter(User.id == current_user.id).with_for_update().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    current_balance = float(user.wallet_balance or 0.0)
    price = float(template.price or 0.0)
    if current_balance < price:
        raise HTTPException(status_code=400, detail="Insufficient wallet balance")

    try:
        user.wallet_balance = current_balance - price
        db.add(user)
        db.flush()
        user_template_repo.create(db, obj_in={"user_id": user.id, "template_id": template.id})
        db.commit()
    except Exception:
        db.rollback()
        raise

    return template


@router.get("/my", response_model=List[TemplateListResponse])
async def list_my_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only return templates the user has purchased (exclude free templates)
    purchased_links = user_template_repo.list_by_user(db, current_user.id)
    purchased_template_ids = [link.template_id for link in purchased_links]
    if not purchased_template_ids:
        return []
    purchased_templates = (
        db.query(Template)
        .filter(Template.id.in_(purchased_template_ids))
        .all()
    )
    # Include purchased flag as True for clarity
    return [
        TemplateListResponse(
            id=tpl.id,
            name=tpl.name,
            description=tpl.description,
            direction=tpl.direction,
            language=tpl.language,
            price=tpl.price,
            is_free=tpl.is_free,
            is_enabled=tpl.is_enabled,
            preview_path=tpl.preview_path,
            category=tpl.category,
            sort_order=tpl.sort_order,
            purchased=True,
        )
        for tpl in purchased_templates
    ]