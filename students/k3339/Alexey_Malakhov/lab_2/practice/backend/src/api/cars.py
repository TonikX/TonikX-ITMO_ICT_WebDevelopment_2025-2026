from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.models.car import Car

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import selectinload

templates = Jinja2Templates(directory="src/templates")
router = APIRouter(prefix="/cars")


@router.get("/detail/{car_id}", response_class=HTMLResponse)
async def car_by_id(car_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Car).where(Car.id_car == car_id).options(selectinload(Car.users)))
    return templates.TemplateResponse("car/car_detailed.html", {"request": request, "car": result.scalars().first()})


@router.get("/all", response_class=HTMLResponse)
async def all_cars(request: Request, session: AsyncSession = Depends(get_session)):
    base_query = select(Car).options(selectinload(Car.users)).order_by(Car.id_car.desc())
    result = await session.execute(base_query)
    return templates.TemplateResponse("car/cars.html", {"request": request, "cars": result.scalars().all()})


@router.get("/edit/{car_id}", response_class=HTMLResponse)
async def edit_car(car_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Car).where(Car.id_car == car_id).options(selectinload(Car.users)))
    return templates.TemplateResponse("car/car_edit.html", {"request": request, "car": result.scalars().first()})


@router.post("/edit/{car_id}")
async def edit_car_submit(car_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    form = await request.form()
    car = await session.get(Car, car_id)
    if not car:
        return RedirectResponse("/cars", status_code=303)

    car.brand = (form.get("brand") or "").strip()  # type: ignore
    car.model = (form.get("model") or "").strip()  # type: ignore
    car.plate = (form.get("plate") or "").strip()  # type: ignore
    car.color = (form.get("color") or "").strip()  # type: ignore

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        return RedirectResponse(f"/cars/edit/{car_id}", status_code=303)

    return RedirectResponse(f"/cars/edit/{car.id_car}", status_code=303)


@router.get("/delete/{car_id}", response_class=HTMLResponse)
async def delete_car(car_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Car).where(Car.id_car == car_id).options(selectinload(Car.users)))
    return templates.TemplateResponse("car/car_delete.html", {"request": request, "car": result.scalars().first()})


@router.post("/delete/{car_id}", response_class=HTMLResponse)
async def delete_car_submit(car_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    car = await session.get(Car, car_id)
    if not car:
        return RedirectResponse("/cars", status_code=303)

    try:
        await session.delete(car)
        await session.commit()
    except Exception:
        await session.rollback()
        return RedirectResponse(f"/cars/delete/{car_id}", status_code=303)

    return RedirectResponse("/cars/all", status_code=303)


@router.get("/add", response_class=HTMLResponse)
async def add_car(request: Request, session: AsyncSession = Depends(get_session)):
    return templates.TemplateResponse("car/car_add.html", {"request": request, "car": None})


@router.post("/add")
async def add_car_submit(request: Request, session: AsyncSession = Depends(get_session)):
    form = await request.form()

    plate = (form.get("plate") or "").strip()  # type: ignore
    brand = (form.get("brand") or "").strip()  # type: ignore
    model = (form.get("model") or "").strip()  # type: ignore
    color = (form.get("color") or "").strip()  # type: ignore

    car = Car(plate=plate, brand=brand, model=model, color=color)
    session.add(car)

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        # при ошибке можно вернуть обратно на форму
        return RedirectResponse("/cars/add", status_code=303)

    return RedirectResponse(f"/cars/detail/{car.id_car}", status_code=303)
