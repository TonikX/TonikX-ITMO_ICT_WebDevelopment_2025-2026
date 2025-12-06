from sqlalchemy import select, delete, func, Select, text, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.schemas import User, Post, Image, Like, Comment
from src.db.utils import post_options


async def paginate(session: AsyncSession, query: Select, limit: int, offset: int) -> dict:
    return {
        'count': await session.scalar(select(func.count()).select_from(query.subquery())),
        'items': [record for record in await session.scalars(query.limit(limit).offset(offset))]
    }


# images:
async def add_image(session: AsyncSession, user_id: int, hash: str, width: int, height: int) -> Image:
    image = Image(hash=hash, width=width, height=height, created_by=user_id)
    session.add(image)
    await session.commit()
    return image


# users:
async def add_user(session: AsyncSession, login: str, name: str, password: str) -> User:
    user = User(login=login, name=name, password=password)
    session.add(user)
    await session.commit()
    return user


async def update_user(session: AsyncSession, id: int, name: str | None = None,
                      about: str | None = None, img_hash: str | None = None) -> User:
    user = await get_user_by_id(session, id)
    if name is not None:
        user.name = name
    if about is not None:
        user.about = about
    if img_hash is not None:
        img = await session.execute(select(Image).where(Image.hash == img_hash))
        user.images = img.scalars().all()
    await session.commit()
    return user


async def get_users(session: AsyncSession, limit, offset):
    stmt = select(User).where(User.is_deleted == 0).options(selectinload(User.images))
    res = await paginate(session, stmt, limit, offset)
    return res


async def get_user_by_id(session: AsyncSession, id: int):
    stmt = select(User).where(User.id == id).options(selectinload(User.images))
    user = await session.scalar(stmt)
    return user


async def get_user_by_login(session: AsyncSession, login: str):
    stmt = select(User).where(User.login == login)
    user = await session.scalar(stmt)
    return user


# posts:


async def add_post(session: AsyncSession, user_id: int, title: str = "",
                   text: str = "", images_hash=[]) -> Post:
    images = await session.execute(select(Image).where(Image.hash.in_(images_hash)))
    user = await get_user_by_id(session, user_id)
    images = images.scalars().all()
    post = Post(
        title=title,
        text=text,
        user=user,
        images=images
    )
    session.add(post)
    await session.commit()
    post.is_liked = False
    post.like_count = 0
    post.comment_count = 0
    return post


async def get_post_by_id(session: AsyncSession, id: int, user_id: int):
    stmt = select(Post).join(Comment, isouter=True).join(Like, isouter=True).where(Post.id == id).options(
        *post_options(user_id)
    ).group_by(Post.id)
    post = await session.scalar(stmt)
    return post


async def get_posts(session: AsyncSession, limit, offset, user_id: int):
    stmt = (
        select(Post).join(Comment, isouter=True).join(Like, isouter=True)
        .options(*post_options(user_id)).where(Post.is_deleted == 0)
        .group_by(Post.id)
        .order_by(Post.created_time.desc())
    )
    res = await paginate(session, stmt, limit, offset)
    return res


async def get_most_liked_posts(session: AsyncSession, limit, offset, user_id: int):
    stmt = (
        select(Post).join(Comment, isouter=True).join(Like, isouter=True)
        .options(*post_options(user_id)).where(Post.is_deleted == 0,
                                               Post.created_time >= text("NOW() - INTERVAL '7 DAY'"))
        .group_by(Post.id)
        .order_by(desc(func.calculate_post_score(Post.id, 1.5, 1.5, 0.0003))))
    res = await paginate(session, stmt, limit, offset)
    return res


async def get_posts_user_id(session: AsyncSession, limit, offset, owner_id: int, user_id):
    stmt = (
        select(Post).join(Comment, isouter=True).join(Like, isouter=True)
        .options(*post_options(user_id)).where(Post.is_deleted == 0, Post.user_id == owner_id)
        .group_by(Post.id)
        .order_by(Post.created_time.desc())
    )
    res = await paginate(session, stmt, limit, offset)
    return res


# async def delete_post(session: AsyncSession, id: int):
#     post = await session.get(Post, id)
#     stmt = update(PostImage).where(PostImage.post_id == id).values(is_deleted=1)
#     await session.execute(stmt)
#     stmt = update(Comment).where(Comment.post_id == id).values(is_deleted=1)
#     await session.execute(stmt)
#     post.is_deleted = 1
#     await session.commit()


# likes
async def set_like(session: AsyncSession, user_id: int, post_id: int):
    insert_stmt = insert(Like).values(user_id=user_id, post_id=post_id).on_conflict_do_nothing()
    await session.execute(insert_stmt)
    await session.commit()


async def delete_like(session: AsyncSession, user_id: int, post_id: int):
    stmt = delete(Like).where(Like.user_id == user_id, Like.post_id == post_id)
    await session.execute(stmt)
    await session.commit()


async def get_count_likes(session: AsyncSession, post_id: int):
    count = await session.scalar(select(func.count())
                                 .select_from(select(Like).where(Like.post_id == post_id).subquery()))
    return count


# comments:
async def get_comments(session: AsyncSession, post_id, limit, offset):
    stmt = select(Comment).where(Comment.post_id == post_id, Comment.is_deleted == 0).options(
        selectinload(Comment.user))
    res = await paginate(session, stmt, limit, offset)
    return res


async def get_count_comments(session: AsyncSession, post_id: int):
    count = await session.scalar(select(func.count()).select_from(
        select(Comment).where(Comment.post_id == post_id, Comment.is_deleted == 0).subquery()))
    return count


async def add_comment(session: AsyncSession, user_id: int, post_id: int, text: str):
    user = await get_user_by_id(session, user_id)
    comment = Comment(
        user=user,
        post_id=post_id,
        text=text
    )
    session.add(comment)
    await session.commit()
    return comment


async def update_comment(session: AsyncSession, comment_id: int, text: str | None = None):
    comment = await session.get(Comment, comment_id)
    comment.text = text
    if text is not None:
        comment.text = text
    await session.commit()


async def delete_comment(session: AsyncSession, comment_id: int):
    await session.execute(delete(Comment).where(Comment.id == comment_id))
    await session.commit()


async def get_comment_by_id(session: AsyncSession, id: int):
    stmt = select(Comment).where(Comment.id == id)
    comment = await session.scalar(stmt)
    return comment
