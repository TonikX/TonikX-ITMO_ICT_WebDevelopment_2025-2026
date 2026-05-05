from sqlmodel import Session

from models import Book
from repos.book import BooksRepository
from repos.user import UsersRepository
from schemas.book import BookUpdate, BookBase


class BooksService:
    def __init__(self, session: Session):
        self.session = session
        self.books_repo = BooksRepository(session)
        self.users_repo = UsersRepository(session)

    def list(self, page: int, size: int) -> dict:
        if page < 1:
            raise ValueError("Page must be >= 1")
        if size < 1 or size > 100:
            raise ValueError("Size must be between 1 and 100")

        offset = (page - 1) * size

        total = self.books_repo.count()
        items = self.books_repo.list(offset=offset, limit=size)

        pages = (total + size - 1) // size

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
        }

    def get(self, book_id: int) -> Book:
        book = self.books_repo.get(book_id)
        if not book:
            raise LookupError("Book not found")
        return book

    def create(self, payload: BookBase, user_id: int) -> Book:
        user = self.users_repo.get(user_id)
        if not user:
            raise LookupError("User not exist")

        data = payload.model_dump(mode="json")
        book = Book(**data, user_id=user_id)

        self.books_repo.add(book)
        self.books_repo.commit()
        self.books_repo.refresh(book)

        return book

    def delete(self, book_id: int, user_id: int) -> None:
        book = self.books_repo.get(book_id)
        if not book:
            raise LookupError("Book not found")

        if book.user_id != user_id:
            raise LookupError("Do not enough rights")

        self.books_repo.delete(book)
        self.books_repo.commit()

    def update(self, book_id: int, payload: BookUpdate, user_id: int) -> Book:
        book = self.books_repo.get(book_id)
        if not book:
            raise LookupError("Book not found")

        if book.user_id != user_id:
            raise LookupError("Do not enough rights")

        data = payload.model_dump(mode="json", exclude_unset=True)
        for key, value in data.items():
            setattr(book, key, value)

        self.books_repo.add(book)
        self.books_repo.commit()
        self.books_repo.refresh(book)

        return book