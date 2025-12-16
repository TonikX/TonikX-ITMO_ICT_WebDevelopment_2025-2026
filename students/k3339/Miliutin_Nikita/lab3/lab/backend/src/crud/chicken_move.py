from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.models import ChickenMove
from src.schemas.chicken_move import ChickenMoveCreate, ChickenMoveUpdate


class CRUDChickenMove:
    def get(self, db: Session, move_id: int) -> Optional[ChickenMove]:
        stmt = select(ChickenMove).where(ChickenMove.move_id == move_id)
        return db.execute(stmt).scalar_one_or_none()

    def get_expanded(self, db: Session, move_id: int) -> Optional[ChickenMove]:
        """
        Для ChickenMoveOutExpanded: подгружаем chicken, from_cage, to_cage.
        """
        stmt = (
            select(ChickenMove)
            .options(
                selectinload(ChickenMove.chicken),
                selectinload(ChickenMove.from_cage),
                selectinload(ChickenMove.to_cage),
            )
            .where(ChickenMove.move_id == move_id)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        chicken_id: Optional[int] = None,
        from_cage_id: Optional[int] = None,
        to_cage_id: Optional[int] = None,
        moved_from: Optional[datetime] = None,
        moved_to: Optional[datetime] = None,
        expanded: bool = False,
        newest_first: bool = True,
    ) -> Sequence[ChickenMove]:
        stmt = select(ChickenMove)

        if expanded:
            stmt = stmt.options(
                selectinload(ChickenMove.chicken),
                selectinload(ChickenMove.from_cage),
                selectinload(ChickenMove.to_cage),
            )

        if chicken_id is not None:
            stmt = stmt.where(ChickenMove.chicken_id == chicken_id)
        if from_cage_id is not None:
            stmt = stmt.where(ChickenMove.from_cage_id == from_cage_id)
        if to_cage_id is not None:
            stmt = stmt.where(ChickenMove.to_cage_id == to_cage_id)

        if moved_from is not None:
            stmt = stmt.where(ChickenMove.moved_at >= moved_from)
        if moved_to is not None:
            stmt = stmt.where(ChickenMove.moved_at <= moved_to)

        order_col = ChickenMove.moved_at.desc() if newest_first else ChickenMove.moved_at.asc()
        stmt = stmt.order_by(order_col, ChickenMove.move_id).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def create_raw(self, db: Session, data: ChickenMoveCreate) -> ChickenMove:
        """
        "Сырой" create (без бизнес-логики).
        Я НЕ рекомендую использовать его для реального перемещения курицы.
        Лучше сервис move_chicken (см. ниже).
        """
        obj = ChickenMove(
            chicken_id=data.chicken_id,
            from_cage_id=data.from_cage_id,
            to_cage_id=data.to_cage_id,
            moved_at=data.moved_at,
            reason=data.reason,
        )
        db.add(obj)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: ChickenMove, data: ChickenMoveUpdate) -> ChickenMove:
        if data.from_cage_id is not None:
            obj.from_cage_id = data.from_cage_id
        if data.to_cage_id is not None:
            obj.to_cage_id = data.to_cage_id
        if data.moved_at is not None:
            obj.moved_at = data.moved_at
        if data.reason is not None:
            obj.reason = data.reason

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj: ChickenMove) -> None:
        db.delete(obj)
        db.commit()
