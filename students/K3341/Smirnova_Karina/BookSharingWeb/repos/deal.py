from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from models import Deal


class DealsRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_with_book(self) -> list[Deal]:
        stmt = select(Deal).options(selectinload(Deal.book))
        return self.session.exec(stmt).all()

    def get_by_id_detail(self, deal_id: int) -> Deal | None:
        stmt = (
            select(Deal)
            .where(Deal.id == deal_id)
            .options(
                selectinload(Deal.owner),
                selectinload(Deal.request_user),
                selectinload(Deal.book),
            )
        )
        return self.session.exec(stmt).first()

    def get(self, deal_id: int) -> Deal | None:
        return self.session.get(Deal, deal_id)

    def find_by_book_id(self, book_id: int) -> Deal | None:
        stmt = select(Deal).where(Deal.book_id == book_id)
        return self.session.exec(stmt).first()

    def list_for_user_detail(self, user_id: int) -> list[Deal]:
        stmt = (
            select(Deal)
            .where((Deal.owner_id == user_id) | (Deal.request_user_id == user_id))
            .order_by(Deal.created_at.desc())
            .options(
                selectinload(Deal.book),
                selectinload(Deal.owner),
                selectinload(Deal.request_user),
            )
        )
        return self.session.exec(stmt).all()

    def add(self, deal: Deal) -> Deal:
        self.session.add(deal)
        return deal

    def delete(self, deal: Deal) -> None:
        self.session.delete(deal)

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, deal: Deal) -> None:
        self.session.refresh(deal)