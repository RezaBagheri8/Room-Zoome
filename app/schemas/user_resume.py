from pydantic import BaseModel
from typing import Optional, List


class UserResume(BaseModel):
    id: int
    file_name: str
    file_path: str
    content_type: str
    file_size_bytes: int
    template_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserResumeListResponse(BaseModel):
    items: List[UserResume]
    total: int


