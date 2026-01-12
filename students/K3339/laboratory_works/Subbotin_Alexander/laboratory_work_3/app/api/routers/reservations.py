from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_async_session
from app.api.schemas import ReservationCreate, ReservationUpdate, ReservationWithTour, ReservationWithTourAndUser, AdminStats
from app.core.db import crud
from app.api.routers.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=ReservationWithTour, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Создание нового бронирования (требуется авторизация).
    Один пользователь = один гость.
    Пользователь может забронировать тур только один раз.
    
    - **tour_id**: ID тура для бронирования
    - **notes**: дополнительные заметки
    """
    # Проверяем, существует ли тур
    tour = await crud.get_tour_by_id(db, reservation_data.tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )
    
    # Проверяем, не бронировал ли пользователь уже этот тур
    existing_reservation = await crud.get_user_reservation_for_tour(
        db, user_id=current_user.id, tour_id=reservation_data.tour_id
    )
    if existing_reservation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already booked this tour"
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
    
    Пользователь может удалять только свои бронирования со статусом "ожидает".
    Нельзя удалять подтвержденные или отклоненные бронирования.
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
    
    # Проверяем статус - можно удалить только ожидающие брони
    if reservation.status != 'pending':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete confirmed or rejected reservations"
        )
    
    await crud.delete_reservation(db, reservation_id)
    return None
    
    await crud.delete_reservation(db, reservation_id)
    return None


# Admin endpoints

@router.get("/admin/all", response_model=List[ReservationWithTourAndUser])
async def get_all_reservations_admin(
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: str | None = Query(None, description="Filter by status: pending, confirmed, rejected"),
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_admin)
):
    """
    [ADMIN] Получение всех бронирований в системе.
    
    - **limit**: количество записей на странице
    - **offset**: смещение для пагинации
    - **status**: фильтр по статусу (pending/confirmed/rejected)
    """
    reservations = await crud.get_all_reservations_admin(
        db, 
        limit=limit,
        offset=offset,
        status=status
    )
    
    # Add username to each reservation
    result = []
    for reservation in reservations:
        res_dict = ReservationWithTourAndUser.model_validate(reservation).model_dump()
        res_dict['username'] = reservation.user.username if reservation.user else None
        result.append(ReservationWithTourAndUser(**res_dict))
    
    return result


@router.put("/admin/{reservation_id}/confirm", response_model=ReservationWithTour)
async def confirm_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_admin)
):
    """
    [ADMIN] Подтверждение бронирования.
    """
    reservation = await crud.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    updated_reservation = await crud.update_reservation(
        db, 
        reservation_id,
        {"status": "confirmed"}
    )
    
    updated_reservation = await crud.get_reservation_by_id(db, reservation_id)
    return updated_reservation


@router.put("/admin/{reservation_id}/reject", response_model=ReservationWithTour)
async def reject_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_admin)
):
    """
    [ADMIN] Отклонение бронирования.
    """
    reservation = await crud.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    updated_reservation = await crud.update_reservation(
        db, 
        reservation_id,
        {"status": "rejected"}
    )
    
    updated_reservation = await crud.get_reservation_by_id(db, reservation_id)
    return updated_reservation


@router.get("/admin/stats", response_model=AdminStats)
async def get_admin_stats(
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_admin)
):
    """
    [ADMIN] Получение статистики продаж.
    
    Возвращает:
    - confirmed_reservations: количество подтверждённых бронирований
    - total_revenue: общая сумма выручки
    - total_customers: количество уникальных клиентов
    """
    stats = await crud.get_admin_stats(db)
    return stats
