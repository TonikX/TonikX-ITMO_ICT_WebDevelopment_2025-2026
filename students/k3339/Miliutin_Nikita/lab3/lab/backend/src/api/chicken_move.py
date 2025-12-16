# src/api/chicken_move.py
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.crud.chicken_move import CRUDChickenMove
from src.database import SessionLocal
from src.schemas.chicken_move import (
    ChickenMoveCreate,
    ChickenMoveOut,
    ChickenMoveOutExpanded,
    ChickenMoveUpdate,
)

router = APIRouter(prefix="/chicken-moves", tags=["ChickenMove"])
crud_move = CRUDChickenMove()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[ChickenMoveOut])
def list_chicken_moves(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),

    chicken_id: Optional[int] = Query(None, ge=1),
    from_cage_id: Optional[int] = Query(None, ge=1),
    to_cage_id: Optional[int] = Query(None, ge=1),

    moved_from: Optional[datetime] = Query(None),
    moved_to: Optional[datetime] = Query(None),

    expanded: bool = Query(False),
    newest_first: bool = Query(True),

    db: Session = Depends(get_db),
):
    # Важно: response_model тут ChickenMoveOut (без вложенных),
    # но expanded=True всё равно подгрузит связи (может быть полезно).
    return list(
        crud_move.list(
            db,
            skip=skip,
            limit=limit,
            chicken_id=chicken_id,
            from_cage_id=from_cage_id,
            to_cage_id=to_cage_id,
            moved_from=moved_from,
            moved_to=moved_to,
            expanded=expanded,
            newest_first=newest_first,
        )
    )


@router.get("/{move_id}", response_model=ChickenMoveOut)
def get_chicken_move(
    move_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_move.get(db, move_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ChickenMove not found")
    return obj


@router.get("/{move_id}/expanded", response_model=ChickenMoveOutExpanded)
def get_chicken_move_expanded(
    move_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_move.get_expanded(db, move_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ChickenMove not found")
    return obj


@router.post("/", response_model=ChickenMoveOut, status_code=status.HTTP_201_CREATED)
def create_chicken_move_raw(
    data: ChickenMoveCreate,
    db: Session = Depends(get_db),
):
    # ты сам в CRUD написал что это "сырой" create.
    # в идеале, реальный move должен также обновлять chicken.cage_id.
    try:
        return crud_move.create_raw(db, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="ChickenMove create conflict (integrity error)")


@router.patch("/{move_id}", response_model=ChickenMoveOut)
def update_chicken_move(
    move_id: int,
    data: ChickenMoveUpdate,
    db: Session = Depends(get_db),
):
    obj = crud_move.get(db, move_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ChickenMove not found")

    try:
        return crud_move.update(db, obj, data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="ChickenMove update conflict (integrity error)")


@router.delete("/{move_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chicken_move(
    move_id: int,
    db: Session = Depends(get_db),
):
    obj = crud_move.get(db, move_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ChickenMove not found")

    crud_move.delete(db, obj)
    return None

