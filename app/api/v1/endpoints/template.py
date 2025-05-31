from fastapi import APIRouter
from typing import Dict, List

router = APIRouter(
    prefix="/template",
    tags=["template"]
)


@router.get("/options", response_model=List[Dict[str, str]])
async def get_template_options():
    """Get available resume template options"""
    templates = [
        {
            "id": "resume_template.html",
            "name": "Persian RTL Template",
            "description": "Right-to-left template with Persian language support",
            "direction": "rtl",
            "language": "Persian"
        },
        {
            "id": "resume_template_ltr.html",
            "name": "English LTR Template",
            "description": "Left-to-right template with English language support",
            "direction": "ltr",
            "language": "English"
        }
    ]
    return templates