from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.auth import get_current_user
from src.database import get_session
from src.models.author import Author
from src.models.subscription import Subscription
from src.models.user import User

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


# Schemas
class SubscriptionCreate(BaseModel):
    author_id: int
    duration_days: int = 30  # По умолчанию 30 дней


class SubscriptionRead(BaseModel):
    id: int
    subscriber_id: int
    author_id: int
    started_at: datetime
    expires_at: datetime | None
    renewable: bool = True

    class Config:
        from_attributes = True


@router.get('/', response_model=List[SubscriptionRead])
async def get_my_subscriptions(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Получить все мои подписки на авторов"""
    query = select(Subscription).where(
        Subscription.subscriber_id == current_user.id
    ).order_by(Subscription.created_at.desc())
    
    result = await session.execute(query)
    subscriptions = result.scalars().all()
    
    return [SubscriptionRead.model_validate(sub) for sub in subscriptions]


@router.get('/{subscription_id}', response_model=SubscriptionRead)
async def get_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Получить информацию о конкретной подписке"""
    subscription = await session.get(Subscription, subscription_id)
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.subscriber_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return SubscriptionRead.model_validate(subscription)


@router.post('/', response_model=SubscriptionRead, status_code=201)
async def create_subscription(
    data: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Подписаться на автора на указанный срок"""
    # Проверяем существование автора
    author = await session.get(Author, data.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Проверяем, что пользователь не пытается подписаться на самого себя
    if author.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot subscribe to yourself")
    
    # Проверяем, не подписан ли уже пользователь
    existing = await session.execute(
        select(Subscription).where(
            Subscription.subscriber_id == current_user.id,
            Subscription.author_id == data.author_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already subscribed to this author")
    
    # Создаем подписку
    expires_at = datetime.utcnow() + timedelta(days=data.duration_days)
    subscription = Subscription(
        subscriber_id=current_user.id,
        author_id=data.author_id,
        started_at=datetime.utcnow(),
        expires_at=expires_at,
        renewable=True
    )
    
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    
    return SubscriptionRead.model_validate(subscription)


@router.put('/{subscription_id}/extend', response_model=SubscriptionRead)
async def extend_subscription(
    subscription_id: int,
    duration_days: int = 30,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Продлить существующую подписку на дополнительное количество дней"""
    subscription = await session.get(Subscription, subscription_id)
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.subscriber_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Продлеваем подписку
    if subscription.expires_at is None:
        # Если бессрочная, устанавливаем новую дату
        subscription.expires_at = datetime.utcnow() + timedelta(days=duration_days)
    else:
        # Если есть дата окончания, добавляем к ней
        subscription.expires_at += timedelta(days=duration_days)
    
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    
    return SubscriptionRead.model_validate(subscription)


@router.put('/{subscription_id}/cancel', response_model=SubscriptionRead)
async def cancel_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Отменить автопродление подписки"""
    subscription = await session.get(Subscription, subscription_id)
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.subscriber_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    subscription.renewable = False
    await session.commit()
    await session.refresh(subscription)
    
    return SubscriptionRead.model_validate(subscription)


@router.put('/{subscription_id}/renew', response_model=SubscriptionRead)
async def renew_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Восстановить автопродление подписки"""
    subscription = await session.get(Subscription, subscription_id)
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.subscriber_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    subscription.renewable = True
    await session.commit()
    await session.refresh(subscription)
    
    return SubscriptionRead.model_validate(subscription)


@router.delete('/{subscription_id}', status_code=204)
async def delete_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Полностью удалить подписку"""
    subscription = await session.get(Subscription, subscription_id)
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    if subscription.subscriber_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    await session.delete(subscription)
    await session.commit()
    
    return None