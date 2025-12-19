from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime

from src.database import get_session
from src.models.user import User
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(prefix="/users")


@router.get("/detail/{user_id}", response_class=HTMLResponse)
async def user_by_id(user_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where(User.id_user == user_id).options(selectinload(User.cars), selectinload(User.licenses))
    )
    return templates.TemplateResponse(
        "user/user_detailed.html",
        {"request": request, "user": result.scalars().first()},
    )


@router.get("/all", response_class=HTMLResponse)
async def all_users(request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).options(selectinload(User.cars)).order_by(User.id_user.desc()))
    return templates.TemplateResponse(
        "user/users.html",
        {"request": request, "users": result.scalars().all()},
    )


@router.get("/edit/{user_id}", response_class=HTMLResponse)
async def edit_user(user_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where(User.id_user == user_id).options(selectinload(User.cars), selectinload(User.licenses))
    )
    return templates.TemplateResponse(
        "user/user_edit.html",
        {"request": request, "user": result.scalars().first()},
    )


@router.post("/edit/{user_id}")
async def edit_user_submit(user_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    form = await request.form()
    user = await session.get(User, user_id)
    if not user:
        return RedirectResponse("/users/all", status_code=303)

    user.last_name = (form.get("last_name") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    user.first_name = (form.get("first_name") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    user.passport_number = (form.get("passport_number") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    user.home_address = (form.get("home_address") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    user.nationality = (form.get("nationality") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]

    bd = (form.get("birth_date") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    user.birth_date = None  # pyright: ignore[reportAttributeAccessIssue]
    if bd:
        try:
            user.birth_date = datetime.fromisoformat(bd)  # pyright: ignore[reportAttributeAccessIssue]
        except ValueError:
            pass

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        return RedirectResponse(f"/users/edit/{user_id}", status_code=303)

    return RedirectResponse(f"/users/detail/{user.id_user}", status_code=303)


@router.get("/delete/{user_id}", response_class=HTMLResponse)
async def delete_user(user_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id_user == user_id).options(selectinload(User.cars)))
    return templates.TemplateResponse(
        "user/user_delete.html",
        {"request": request, "user": result.scalars().first()},
    )


@router.post("/delete/{user_id}")
async def delete_user_submit(user_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        return RedirectResponse("/users/all", status_code=303)
    try:
        await session.delete(user)
        await session.commit()
    except Exception:
        await session.rollback()
        return RedirectResponse(f"/users/delete/{user_id}", status_code=303)
    return RedirectResponse("/users/all", status_code=303)


@router.get("/add", response_class=HTMLResponse)
async def add_user(request: Request, session: AsyncSession = Depends(get_session)):
    return templates.TemplateResponse("user/user_add.html", {"request": request, "user": None})


@router.post("/add")
async def add_user_submit(request: Request, session: AsyncSession = Depends(get_session)):
    form = await request.form()
    last_name = (form.get("last_name") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    first_name = (form.get("first_name") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    passport_number = (form.get("passport_number") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    home_address = (form.get("home_address") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    nationality = (form.get("nationality") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]

    bd = (form.get("birth_date") or "").strip()  # pyright: ignore[reportAttributeAccessIssue]
    birth_date = None
    if bd:
        try:
            birth_date = datetime.fromisoformat(bd)
        except ValueError:
            pass

    user = User(
        last_name=last_name,
        first_name=first_name,
        birth_date=birth_date,
        passport_number=passport_number,
        home_address=home_address,
        nationality=nationality,
    )
    session.add(user)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        return RedirectResponse("/users/add", status_code=303)

    return RedirectResponse(f"/users/detail/{user.id_user}", status_code=303)
