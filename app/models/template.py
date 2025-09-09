from sqlalchemy import Column, String, Boolean, Integer, Float, Text
from app.models.base import Base


class Template(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    direction = Column(String(10), nullable=False, default="ltr")  # ltr or rtl
    language = Column(String(50), nullable=False, default="English")
    price = Column(Float, nullable=False, default=0.0)
    is_free = Column(Boolean, nullable=False, default=True)
    is_enabled = Column(Boolean, nullable=False, default=True)
    template_path = Column(String(255), nullable=False)  # Relative path to HTML template file
    preview_path = Column(String(255), nullable=True)  # Relative path to preview image
    category = Column(String(50), nullable=True)  # Optional category for grouping templates
    sort_order = Column(Integer, nullable=False, default=0)  # For ordering templates in lists
