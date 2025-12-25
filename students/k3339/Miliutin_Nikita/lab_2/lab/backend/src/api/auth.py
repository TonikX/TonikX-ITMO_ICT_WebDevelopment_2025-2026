from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import config, security
from src.database import get_session
from src.models.user import User
from src.passcrypt import hash_password, verify_password

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    query = await session.execute(select(User).where(User.email == email))
    result = query.scalars().first()

    if not result or not verify_password(password, result.password_hash):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Неверный email или пароль"},
        )

    token = security.create_access_token(uid=str(result.id_user))

    response = RedirectResponse(url="/flights", status_code=303)
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # True если HTTPS
    )
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/reg.html", {"request": request})


@router.post("/register")
async def register_post(
    last_name: str = Form(...),
    first_name: str = Form(...),
    patronymic: str = Form(None),
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    existing = await session.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    print("TYPE:", type(password))
    print("RAW:", repr(password))
    print("LEN:", len(password.encode()))

    user = User(
        last_name=last_name,
        first_name=first_name,
        patronymic=patronymic,
        email=email,
        password_hash=hash_password(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    token = security.create_access_token(uid=str(user.id_user))

    response = RedirectResponse(url="/flights", status_code=303)
    response.set_cookie(key=config.JWT_ACCESS_COOKIE_NAME, value=token, httponly=True, samesite="lax", secure=False)
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/flights", status_code=303)
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return response
