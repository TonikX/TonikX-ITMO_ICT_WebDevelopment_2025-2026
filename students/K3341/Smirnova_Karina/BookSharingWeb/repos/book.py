from sqlalchemy import func
from sqlmodel import Session, select

from models import Book


class BooksRepository:
    def __init__(self, session: Session):
        self.session = session

    def count(self) -> int:
        return self.session.exec(select(func.count()).select_from(Book)).one()

    def list(self, *, offset: int, limit: int) -> list[Book]:
        return self.session.exec(
            select(Book).offset(offset).limit(limit)
        ).all()

    def get(self, book_id: int) -> Book | None:
        return self.session.get(Book, book_id)

    def add(self, book: Book) -> Book:
        self.session.add(book)
        return book

    def delete(self, book: Book) -> None:
        self.session.delete(book)

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, book: Book) -> None:
        self.session.refresh(book)