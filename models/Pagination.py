from typing import List

from pydantic import BaseModel

from models.User import User


class PaginatedUsers(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[User]