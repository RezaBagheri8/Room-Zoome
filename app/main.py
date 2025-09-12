from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer

from app.api.v1.api import api_router
from app.core.config import API_V1_STR
from app.db.session import engine, Base, SessionLocal
from app.models.base import Base as ModelsBase
from sqlalchemy.orm import Session
from app.models.admin import Admin
import hashlib
import logging

# Create database tables (ensure models Base is applied)
ModelsBase.metadata.create_all(bind=engine)

app = FastAPI(
    title="API with JWT Authentication",
    description="API using JWT Bearer token authentication",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication endpoints"},
        {"name": "protected", "description": "Protected endpoints requiring authentication"},
    ]
)

# Configure OpenAPI security schema
security_scheme = HTTPBearer(
    scheme_name="JWT",
    description="Enter JWT token in the format: Bearer <token>"
)

# Add security scheme to OpenAPI schema
app.openapi_components = {
    "securitySchemes": {
        "JWT": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "in": "header"  # This is the correct way to specify 'in'
        }}
}

# Add security requirement to all endpoints
app.openapi_security = [{"JWT": []}]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def _hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def _seed_admin() -> None:
    db: Session = SessionLocal()
    try:
        username = "admin"
        existing = db.query(Admin).filter(Admin.username == username).first()
        if not existing:
            admin = Admin(
                full_name="Default Admin",
                username=username,
                password_hash=_hash_password("admin123")
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

# Include API router with version prefix
app.include_router(api_router, prefix=API_V1_STR)

# Seed default admin
_seed_admin()


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')