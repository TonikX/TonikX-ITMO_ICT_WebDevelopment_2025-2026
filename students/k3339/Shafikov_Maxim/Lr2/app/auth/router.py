from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.users import UserCreate
from app.crud.users import user_repo
from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_user(
        request: Request,
        db: Session = Depends(get_db),
        email: str = Form(),
        full_name: str = Form(),
        password: str = Form()
):
    user = user_repo.get_by_email(db, email=email)
    if user:
        return templates.TemplateResponse("register.html", {
            "request": request, "error": "Пользователь с таким email уже существует"
        })

    user_in = UserCreate(email=email, full_name=full_name, password=password)
    user_repo.create(db, user=user_in)

    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_for_access_token(
        request: Request,
        db: Session = Depends(get_db),
        username: str = Form(),
        password: str = Form()
):
    user = user_repo.get_by_email(db, email=username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request, "error": "Неверный email или пароль"
        })

    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response