from pydantic import BaseModel


class TopAuthorSchema(BaseModel):
    author_id: int
    author_name: str
    author_handle: str
    subscribers_count: int
    posts_count: int
    avg_engagement_per_post: float
    is_verified: bool

    class Config:
        from_attributes = True


class AuthorsBySubscribersSchema(BaseModel):
    author_id: int
    author_name: str
    author_handle: str
    subscribers_count: int

    class Config:
        from_attributes = True


class AuthorEngagementSchema(BaseModel):
    author_id: int
    author_name: str
    author_handle: str
    avg_likes: float
    avg_comments: float
    total_engagement: float  # avg_likes + avg_comments
    posts_count: int
    subscribers_count: int
    engagement_rate: float  # total_engagement / subscribers_count

    class Config:
        from_attributes = True


class TopUserSchema(BaseModel):
    user_id: int
    user_name: str
    likes_given: int
    comments_made: int
    activity_score: int  # likes_given + comments_made

    class Config:
        from_attributes = True


class TopPostSchema(BaseModel):
    post_id: int
    post_text: str | None
    author_name: str
    likes_count: int
    comments_count: int
    total_reactions: int

    class Config:
        from_attributes = True


class PaidContentRatioSchema(BaseModel):
    author_id: int
    author_name: str
    author_handle: str
    free_posts_count: int
    paid_posts_count: int
    total_posts_count: int
    paid_ratio: float  # paid_posts_count / total_posts_count

    class Config:
        from_attributes = True