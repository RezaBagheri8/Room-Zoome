from typing import List
from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from app.models.user_resume import UserResume as UserResumeModel


class UserResumeRepository(BaseRepository[UserResumeModel, UserResumeModel, UserResumeModel]):
    def __init__(self):
        super().__init__(UserResumeModel)

    def list_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[UserResumeModel]:
        return (
            db.query(UserResumeModel)
            .filter(UserResumeModel.user_id == user_id)
            .order_by(UserResumeModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_user(self, db: Session, user_id: int) -> int:
        return db.query(UserResumeModel).filter(UserResumeModel.user_id == user_id).count()


