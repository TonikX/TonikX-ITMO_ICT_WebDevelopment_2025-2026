from pydantic import BaseModel
from typing import List
from src.schemas.post import PostRead


class PaginationInfo(BaseModel):
    totalPages: int
    totalItems: int
    hasMore: bool
    currentPage: int


class PostsResponse(BaseModel):
    posts: List[PostRead]
    pagination: PaginationInfo