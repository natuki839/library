from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserPK(BaseModel):
    user_id: int


class UserBody(BaseModel):
    name: str
    email: str
    is_active: bool = True
    created_at: datetime


class UserRow(UserPK, UserBody):
    pass