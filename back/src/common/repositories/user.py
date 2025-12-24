from src.common.models.user import UserBody, UserPK, UserRow
from src.common.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    table_name = "users"
    pk_model = UserPK
    body_model = UserBody
    row_model = UserRow
