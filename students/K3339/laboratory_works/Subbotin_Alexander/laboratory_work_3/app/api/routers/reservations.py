from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_async_session
from app.api.schemas import ReservationCreate, ReservationUpdate, ReservationWithTour
from app.core.db import crud
from app.api.routers.auth import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=ReservationWithTour, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Создание нового бронирования (требуется авторизация).
    
    - **tour_id**: ID тура для бронирования
    - **guests**: количество гостей
    - **notes**: дополнительные заметки
    """
    # Проверяем, существует ли тур
    tour = await crud.get_tour_by_id(db, reservation_data.tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )
    
    reservation = await crud.create_reservation(
        db, 
        user_id=current_user.id,
        reservation_data=reservation_data.model_dump()
    )
    
    # Перезагружаем с tour
    reservation = await crud.get_reservation_by_id(db, reservation.id)
    return reservation


@router.get("/my", response_model=List[ReservationWithTour])
async def get_my_reservations(
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Получение всех бронирований текущего пользователя.
    
    - **limit**: количество записей на странице
    - **offset**: смещение для пагинации
    """
    reservations = await crud.get_reservations_by_user(
        db, 
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    return reservations


@router.get("/{reservation_id}", response_model=ReservationWithTour)
async def get_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Получение информации о конкретном бронировании.
    
    Пользователь может просматривать только свои бронирования.
    """
    reservation = await crud.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    # Проверяем, что бронирование принадлежит текущему пользователю
    if reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this reservation"
        )
    
    return reservation


@router.put("/{reservation_id}", response_model=ReservationWithTour)
async def update_reservation(
    reservation_id: int,
    reservation_data: ReservationUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Обновление бронирования.
    
    Пользователь может обновлять только свои бронирования.
    """
    reservation = await crud.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    if reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this reservation"
        )
    
    updated_reservation = await crud.update_reservation(
        db, 
        reservation_id,
        reservation_data.model_dump(exclude_unset=True)
    )
    
    # Перезагружаем с tour
    updated_reservation = await crud.get_reservation_by_id(db, reservation_id)
    return updated_reservation


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Удаление бронирования.
    
    Пользователь может удалять только свои бронирования.
    """
    reservation = await crud.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    if reservation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this reservation"
        )
    
    await crud.delete_reservation(db, reservation_id)
    return None
