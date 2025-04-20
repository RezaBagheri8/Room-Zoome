from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer

from app.api.v1.api import api_router
from app.core.config import API_V1_STR
from app.db.session import engine, Base
import logging

# Create database tables
Base.metadata.create_all(bind=engine)

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

# Include API router with version prefix
app.include_router(api_router, prefix=API_V1_STR)


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')