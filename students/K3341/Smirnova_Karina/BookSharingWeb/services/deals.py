from sqlmodel import Session

from models import Deal
from repos.book import BooksRepository
from repos.deal import DealsRepository
from repos.user import UsersRepository
from schemas.deal import DealCreate, DealUpdate


class DealsService:
    def __init__(self, session: Session):
        self.session = session
        self.deals_repo = DealsRepository(session)
        self.users_repo = UsersRepository(session)
        self.books_repo = BooksRepository(session)

    def list(self) -> list[Deal]:
        return self.deals_repo.list_with_book()

    def get_detail(self, deal_id: int, user_id: int) -> Deal:
        deal = self.deals_repo.get_by_id_detail(deal_id)
        if not deal:
            raise LookupError("Deal not found")
        if deal.owner_id != user_id and deal.request_user_id != user_id:
            raise LookupError("Do not enough rights")

        return deal

    def create(self, payload: DealCreate, user_id: int) -> Deal:
        user_owner = self.users_repo.get(payload.owner_id)
        if not user_owner:
            raise LookupError("User owner not exist")

        user_request = self.users_repo.get(payload.request_user_id)
        if not user_request:
            raise LookupError("User request not exist")

        book = self.books_repo.get(payload.book_id)
        if not book:
            raise LookupError("Book not exist")

        if book.user_id != payload.owner_id:
            raise LookupError("Owner do not have this book")

        deal_if_exist = self.deals_repo.find_by_book_id(payload.book_id)
        if deal_if_exist:
            raise ValueError("Deal for this book already exist")

        if user_request.id != user_id:
            raise LookupError("Do not enough rights")

        deal = Deal(**payload.model_dump(mode="json"))
        self.deals_repo.add(deal)
        self.deals_repo.commit()
        self.deals_repo.refresh(deal)
        return deal

    def delete(self, deal_id: int, user_id: int) -> None:
        deal = self.deals_repo.get(deal_id)
        if not deal:
            raise LookupError("Deal not found")

        if deal.request_user_id != user_id:
            raise LookupError("Do not enough rights")

        self.deals_repo.delete(deal)
        self.deals_repo.commit()

    def update(self, deal_id: int, payload: DealUpdate, user_id: int) -> Deal:
        deal = self.deals_repo.get(deal_id)
        if not deal:
            raise LookupError("Deal not found")
        if deal.owner_id != user_id and deal.request_user_id != user_id:
            raise LookupError("Do not enough rights")

        data = payload.model_dump(mode="json", exclude_unset=True)
        for key, value in data.items():
            setattr(deal, key, value)

        self.deals_repo.add(deal)
        self.deals_repo.commit()
        self.deals_repo.refresh(deal)
        return deal