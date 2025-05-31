from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, resume, pdf, template

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(users.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(pdf.router)
api_router.include_router(template.router)