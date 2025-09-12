from typing import List, Optional

from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.models.user_template import UserTemplate


class UserTemplateRepository(BaseRepository[UserTemplate, dict, dict]):
    def __init__(self):
        super().__init__(UserTemplate)

    def get_by_user_and_template(self, db: Session, user_id: int, template_id: int) -> Optional[UserTemplate]:
        return (
            db.query(UserTemplate)
            .filter(UserTemplate.user_id == user_id, UserTemplate.template_id == template_id)
            .first()
        )

    def list_by_user(self, db: Session, user_id: int) -> List[UserTemplate]:
        return (
            db.query(UserTemplate)
            .filter(UserTemplate.user_id == user_id)
            .order_by(UserTemplate.id.desc())
            .all()
        )


