from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.models.base import Base


class UserResume(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    template_id = Column(Integer, ForeignKey("template.id"), nullable=True, index=True)
    file_path = Column(String(512), nullable=False)
    file_name = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False, default="application/pdf")
    file_size_bytes = Column(BigInteger, nullable=False, default=0)

    user = relationship("User")
    template = relationship("Template")


