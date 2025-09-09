from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate
from app.repositories.base import BaseRepository


class TemplateRepository(BaseRepository[Template, TemplateCreate, TemplateUpdate]):
    def __init__(self):
        super().__init__(Template)

    def get_all_templates(self, db: Session) -> List[Template]:
        """Get all templates"""
        return db.query(self.model).order_by(self.model.sort_order.asc(), self.model.name.asc()).all()

    def get_enabled_templates(self, db: Session, skip: int = 0, limit: int = 100) -> List[Template]:
        """Get all enabled templates ordered by sort_order and name"""
        return (
            db.query(self.model)
            .filter(self.model.is_enabled == True)
            .order_by(self.model.sort_order.asc(), self.model.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_free_templates(self, db: Session, skip: int = 0, limit: int = 100) -> List[Template]:
        """Get all free and enabled templates"""
        return (
            db.query(self.model)
            .filter(and_(self.model.is_enabled == True, self.model.is_free == True))
            .order_by(self.model.sort_order.asc(), self.model.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_paid_templates(self, db: Session, skip: int = 0, limit: int = 100) -> List[Template]:
        """Get all paid and enabled templates"""
        return (
            db.query(self.model)
            .filter(and_(self.model.is_enabled == True, self.model.is_free == False))
            .order_by(self.model.sort_order.asc(), self.model.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_category(self, db: Session, category: str, skip: int = 0, limit: int = 100) -> List[Template]:
        """Get templates by category"""
        return (
            db.query(self.model)
            .filter(and_(self.model.is_enabled == True, self.model.category == category))
            .order_by(self.model.sort_order.asc(), self.model.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_name(self, db: Session, name: str) -> Optional[Template]:
        """Get template by name"""
        return db.query(self.model).filter(self.model.name == name).first()

    def toggle_status(self, db: Session, template_id: int) -> Optional[Template]:
        """Toggle the enabled status of a template"""
        template = self.get(db, template_id)
        if template:
            template.is_enabled = not template.is_enabled
            db.commit()
            db.refresh(template)
        return template

    def update_sort_order(self, db: Session, template_id: int, sort_order: int) -> Optional[Template]:
        """Update the sort order of a template"""
        template = self.get(db, template_id)
        if template:
            template.sort_order = sort_order
            db.commit()
            db.refresh(template)
        return template
