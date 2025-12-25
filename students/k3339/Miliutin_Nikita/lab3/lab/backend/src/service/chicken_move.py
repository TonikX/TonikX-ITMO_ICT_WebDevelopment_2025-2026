from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models import Chicken, ChickenMove
from src.schemas.chicken_move import ChickenMoveCreate


class ChickenMoveError(Exception):
    """Базовая ошибка доменной логики перемещений."""


class ChickenNotFoundError(ChickenMoveError):
    pass


class InvalidMoveError(ChickenMoveError):
    pass


def move_chicken(db: Session, data: ChickenMoveCreate) -> ChickenMove:
    """
    Создаёт запись ChickenMove и обновляет Chicken.cage_id (одна транзакция).

    Правила:
    - from_cage_id берём из текущей клетки курицы (Chicken.cage_id)
    - если data.from_cage_id передан и не совпадает с текущим -> ошибка
    - to_cage_id не должен быть равен текущему cage_id (иначе бессмысленно)
    """
    chicken = db.execute(
        select(Chicken).where(Chicken.chicken_id == data.chicken_id)
    ).scalar_one_or_none()

    if chicken is None:
        raise ChickenNotFoundError(f"Chicken {data.chicken_id} not found")

    current_cage_id = chicken.cage_id

    if data.from_cage_id is not None and data.from_cage_id != current_cage_id:
        raise InvalidMoveError(
            f"from_cage_id={data.from_cage_id} не совпадает с текущей клеткой курицы ({current_cage_id})"
        )

    if data.to_cage_id == current_cage_id:
        raise InvalidMoveError("to_cage_id равен текущей клетке — перемещение не требуется")

    move = ChickenMove(
        chicken_id=data.chicken_id,
        from_cage_id=current_cage_id,   # фиксируем откуда реально уехали
        to_cage_id=data.to_cage_id,
        moved_at=data.moved_at,
        reason=data.reason,
    )

    chicken.cage_id = data.to_cage_id  # обновляем текущую клетку

    db.add(move)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(move)
    return move
