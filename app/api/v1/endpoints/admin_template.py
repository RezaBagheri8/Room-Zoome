from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from pathlib import Path
from uuid import uuid4

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


# Helper function to save uploaded files
async def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    """Save an uploaded file to the specified folder and return the relative path"""
    # Create folder if it doesn't exist
    upload_folder = Path(f"app/static/{folder}")
    upload_folder.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = upload_folder / unique_filename
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    # Return relative path for database storage
    return f"/static/{folder}/{unique_filename}"

@router.post("/", response_model=TemplateResponse)
async def create_template(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    direction: str = Form("ltr"),
    language: str = Form("English"),
    price: float = Form(0.0),
    is_free: bool = Form(True),
    is_enabled: bool = Form(True),
    category: Optional[str] = Form(None),
    sort_order: int = Form(0),
    template_file: UploadFile = File(...),
    preview_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Create a new template (Admin only)"""
    try:
        # Check if template with same name already exists
        existing_template = template_repo.get_by_name(db, name)
        if existing_template:
            raise HTTPException(status_code=400, detail="Template with this name already exists")
        
        # Save template file
        template_path = await save_upload_file(template_file, "uploads/templates")
        
        # Save preview file if provided
        preview_path = None
        if preview_file:
            preview_path = await save_upload_file(preview_file, "uploads/previews")
        
        # Create template data object
        template_data = TemplateCreate(
            name=name,
            description=description,
            direction=direction,
            language=language,
            price=price,
            is_free=is_free,
            is_enabled=is_enabled,
            template_path=template_path,
            preview_path=preview_path,
            category=category,
            sort_order=sort_order
        )
        
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
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    direction: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    is_free: Optional[bool] = Form(None),
    is_enabled: Optional[bool] = Form(None),
    category: Optional[str] = Form(None),
    sort_order: Optional[int] = Form(None),
    template_file: Optional[UploadFile] = File(None),
    preview_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permissions)
):
    """Update a template (Admin only)"""
    try:
        template = template_repo.get(db, template_id)
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Check if name is being updated and if it conflicts with existing template
        if name and name != template.name:
            existing_template = template_repo.get_by_name(db, name)
            if existing_template:
                raise HTTPException(status_code=400, detail="Template with this name already exists")
        
        # Create update data dictionary
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if direction is not None:
            update_data["direction"] = direction
        if language is not None:
            update_data["language"] = language
        if price is not None:
            update_data["price"] = price
        if is_free is not None:
            update_data["is_free"] = is_free
        if is_enabled is not None:
            update_data["is_enabled"] = is_enabled
        if category is not None:
            update_data["category"] = category
        if sort_order is not None:
            update_data["sort_order"] = sort_order
            
        # Handle file uploads if provided
        if template_file:
            template_path = await save_upload_file(template_file, "uploads/templates")
            update_data["template_path"] = template_path
            
        if preview_file:
            preview_path = await save_upload_file(preview_file, "uploads/previews")
            update_data["preview_path"] = preview_path
        
        # Create TemplateUpdate object from the update data
        template_data = TemplateUpdate(**update_data)
        
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


@router.put("/{template_id}/toggle-status", response_model=TemplateResponse)
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


@router.put("/{template_id}/sort-order", response_model=TemplateResponse)
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
