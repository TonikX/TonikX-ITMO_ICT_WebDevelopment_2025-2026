from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.database import get_async_session
from app.api.schemas import TourCreate, TourUpdate, TourResponse
from app.core.db import crud
from app.api.routers.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/tours", tags=["Tours"])


@router.post("/", response_model=TourResponse, status_code=status.HTTP_201_CREATED)
async def create_tour(
    tour_data: TourCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_admin)
):
    """
    Создание нового тура (требуется права администратора).
    
    - **title**: название тура
    - **agency**: название агентства
    - **description**: описание тура
    - **start_date**: дата начала
    - **end_date**: дата окончания
    - **price**: цена
    - **city**: город
    - **payment_terms**: условия оплаты (опционально)
    """
    tour = await crud.create_tour(db, tour_data.model_dump())
    return tour


@router.get("/", response_model=List[TourResponse])
async def get_tours(
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    city: Optional[str] = Query(None, description="Фильтр по городу"),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получение списка всех туров с пагинацией и фильтрацией.
    
    - **limit**: количество туров на странице (1-100)
    - **offset**: смещение для пагинации
    - **city**: фильтр по городу (опционально)
    """
    tours = await crud.get_tours(db, limit=limit, offset=offset, city=city)
    return tours


@router.get("/{tour_id}", response_model=TourResponse)
async def get_tour(
    tour_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получение информации о конкретном туре по ID.
    """
    tour = await crud.get_tour_by_id(db, tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )
    return tour


@router.put("/{tour_id}", response_model=TourResponse)
async def update_tour(
    tour_id: int,
    tour_data: TourUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_admin)
):
    """
    Обновление информации о туре (требуется права администратора).
    
    Можно обновить любые поля тура.
    """
    tour = await crud.update_tour(db, tour_id, tour_data.model_dump(exclude_unset=True))
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )
    return tour


@router.delete("/{tour_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tour(
    tour_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_admin)
):
    """
    Удаление тура (требуется права администратора).
    """
    deleted = await crud.delete_tour(db, tour_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )
    return None
