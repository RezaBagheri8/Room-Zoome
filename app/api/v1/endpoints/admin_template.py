from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.repositories.template import TemplateRepository
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/admin/template",
    tags=["admin-template"]
)

template_repo = TemplateRepository()


# TODO: Add admin role check when admin role is implemented
# For now, we'll use a simple check - you can enhance this later
def check_admin_permissions(current_user: User = Depends(get_current_user)):
    # Placeholder for admin role check
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.post("/", response_model=TemplateResponse)
async def create_template(
    template_data: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Create a new template (Admin only)"""
    try:
        # Check if template with same name already exists
        existing_template = template_repo.get_by_name(db, template_data.name)
        if existing_template:
            raise HTTPException(status_code=400, detail="Template with this name already exists")
        
        template = template_repo.create(db, obj_in=template_data)
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating template: {str(e)}")


@router.get("/", response_model=List[TemplateResponse])
async def get_all_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    enabled_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Get all templates with admin details (Admin only)"""
    try:
        if category:
            templates = template_repo.get_by_category(db, category, skip, limit)
        elif enabled_only:
            templates = template_repo.get_enabled_templates(db, skip, limit)
        else:
            templates = template_repo.get_multi(db, skip=skip, limit=limit)
        
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching templates: {str(e)}")


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template_admin(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Get a specific template with admin details (Admin only)"""
    template = template_repo.get(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: int,
    template_data: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Update a template (Admin only)"""
    try:
        template = template_repo.get(db, template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Check if name is being updated and if it conflicts with existing template
        if template_data.name and template_data.name != template.name:
            existing_template = template_repo.get_by_name(db, template_data.name)
            if existing_template:
                raise HTTPException(status_code=400, detail="Template with this name already exists")
        
        updated_template = template_repo.update(db, db_obj=template, obj_in=template_data)
        return updated_template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating template: {str(e)}")


@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Delete a template (Admin only)"""
    try:
        template = template_repo.get(db, template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        template_repo.remove(db, id=template_id)
        return {"message": "Template deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting template: {str(e)}")


@router.patch("/{template_id}/toggle-status", response_model=TemplateResponse)
async def toggle_template_status(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Toggle template enabled/disabled status (Admin only)"""
    try:
        template = template_repo.toggle_status(db, template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error toggling template status: {str(e)}")


@router.patch("/{template_id}/sort-order", response_model=TemplateResponse)
async def update_template_sort_order(
    template_id: int,
    sort_order: int = Query(..., ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Update template sort order (Admin only)"""
    try:
        template = template_repo.update_sort_order(db, template_id, sort_order)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating sort order: {str(e)}")
