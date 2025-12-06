from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.posts.models import PostAdd, PostResponse, PostsListResponse, CommentAdd, CommentResponse, \
    CommentListResponse
from src.api.security import access_policy
from src.api.sessions import get_db_session
from src.db.crud import get_posts, get_post_by_id, add_post, add_comment, delete_comment, get_comment_by_id, \
    get_comments, set_like, delete_like, get_posts_user_id, get_most_liked_posts

router = APIRouter(
    prefix='/post',
    dependencies=[Depends(access_policy)]
)


@router.post("/add", response_model=PostResponse, tags=["posts"])
async def add(post: PostAdd, session: AsyncSession = Depends(get_db_session), credentials=Depends(access_policy)):
    res = await add_post(session, credentials.subject['id'], post.title, post.text, post.images)
    return res


@router.get("/latests", response_model=PostsListResponse, tags=["posts"])
async def get_posts_list(session: AsyncSession = Depends(get_db_session), page: int = Query(1, ge=1),
                         per_page: int = Query(100, ge=0), credentials=Depends(access_policy)):
    limit = per_page * page
    offset = (page - 1) * per_page
    res = await get_posts(session, limit, offset, user_id=credentials.subject['id'])

    return res


@router.get("/recommended", response_model=PostsListResponse, tags=["posts"])
async def get_recommended_posts(session: AsyncSession = Depends(get_db_session), page: int = Query(1, ge=1),
                                per_page: int = Query(100, ge=0), credentials=Depends(access_policy)):
    limit = per_page * page
    offset = (page - 1) * per_page
    res = await get_most_liked_posts(session, limit, offset, user_id=credentials.subject['id'])

    return res


@router.get("/user/{id:int}", response_model=PostsListResponse, tags=["posts"])
async def get_user_posts(id: int, session: AsyncSession = Depends(get_db_session), page: int = Query(1, ge=1),
                         per_page: int = Query(100, ge=0), credentials=Depends(access_policy)):
    limit = per_page * page
    offset = (page - 1) * per_page
    res = await get_posts_user_id(session, limit, offset, owner_id=id, user_id=credentials.subject['id'])

    return res


@router.get("/{id:int}", response_model=PostResponse, tags=["posts"])
async def get_post(id: int, session: AsyncSession = Depends(get_db_session), credentials=Depends(access_policy)):
    res = await get_post_by_id(session, id, credentials.subject['id'])
    return res


@router.post("/{id:int}/like", tags=['likes'])
async def like_post(id: int, session: AsyncSession = Depends(get_db_session), credentials=Depends(access_policy)):
    await set_like(session, credentials.subject['id'], id)
    return 'ok'


@router.delete("/{id:int}/like", tags=['likes'])
async def delete(id: int, session: AsyncSession = Depends(get_db_session), credentials=Depends(access_policy)):
    await delete_like(session, credentials.subject['id'], id)
    return 'ok'


@router.post("/{id:int}/comment", response_model=CommentResponse, tags=['comments'])
async def comment_post(id: int, comment: CommentAdd, session: AsyncSession = Depends(get_db_session),
                       credentials=Depends(access_policy)):
    return await add_comment(session, credentials.subject['id'], id, comment.text)


@router.get("/{id:int}/comments", response_model=CommentListResponse, tags=['comments'])
async def get_comments_post(id: int, session: AsyncSession = Depends(get_db_session),
                            credentials=Depends(access_policy), page: int = Query(1, ge=1),
                            per_page: int = Query(100, ge=0)):
    limit = per_page * page
    offset = (page - 1) * per_page
    return await get_comments(session, id, limit, offset)


@router.delete("/{id:int}/comment/{comment_id:int}", tags=['comments'])
async def delete_comment_post(id: int, comment_id: int, session: AsyncSession = Depends(get_db_session),
                              credentials=Depends(access_policy)):
    comment = await get_comment_by_id(session, comment_id)
    if comment.user_id != credentials.subject['id']:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this comment")
    if comment.post_id != id:
        raise HTTPException(status_code=404, detail="Comment not found")
    await delete_comment(session, comment_id)
    return 'ok'
