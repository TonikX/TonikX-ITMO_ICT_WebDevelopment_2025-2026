from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_async_session
from app.api.schemas import ReviewCreate, ReviewUpdate, ReviewResponse, ReviewWithUser
from app.core.db import crud
from app.api.routers.auth import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Создание нового отзыва на тур (требуется авторизация).
    
    - **tour_id**: ID тура
    - **text**: текст отзыва
    - **rating**: оценка от 1 до 10
    """
    # Проверяем, существует ли тур
    tour = await crud.get_tour_by_id(db, review_data.tour_id)
    if not tour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found"
        )
    
    review = await crud.create_review(
        db,
        user_id=current_user.id,
        review_data=review_data.model_dump()
    )
    return review


@router.get("/tour/{tour_id}", response_model=List[ReviewWithUser])
async def get_tour_reviews(
    tour_id: int,
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получение всех отзывов для конкретного тура.
    
    - **tour_id**: ID тура
    - **limit**: количество отзывов на странице
    - **offset**: смещение для пагинации
    """
    reviews = await crud.get_reviews_by_tour(
        db,
        tour_id=tour_id,
        limit=limit,
        offset=offset
    )
    
    # Добавляем username к каждому отзыву
    result = []
    for review in reviews:
        review_dict = ReviewWithUser.model_validate(review).model_dump()
        review_dict['username'] = review.user.username if review.user else None
        result.append(ReviewWithUser(**review_dict))
    
    return result


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получение информации о конкретном отзыве по ID.
    """
    review = await crud.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return review


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_data: ReviewUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Обновление отзыва.
    
    Пользователь может обновлять только свои отзывы.
    """
    review = await crud.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this review"
        )
    
    updated_review = await crud.update_review(
        db,
        review_id,
        review_data.model_dump(exclude_unset=True)
    )
    return updated_review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(get_current_user)
):
    """
    Удаление отзыва.
    
    Пользователь может удалять только свои отзывы.
    """
    review = await crud.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )
    
    await crud.delete_review(db, review_id)
    return None
