from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.auth import AuthManager
from connection import get_session
from models import User
from schemas.book import (
    BookResponse,
    BookDetailResponse,
    BookUpdate, BookBase,
)
from services.books import BooksService

router = APIRouter(prefix="/books", tags=["books"])
auth_manager = AuthManager()


@router.get("/", response_model=dict)
def book_list(page: int = 1, size: int = 10, session: Session = Depends(get_session)):
    service = BooksService(session)
    try:
        return service.list(page=page, size=size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{book_id}", response_model=BookDetailResponse)
def book_by_id(book_id: int, session: Session = Depends(get_session)):
    service = BooksService(session)
    try:
        return service.get(book_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookBase, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    service = BooksService(session)
    try:
        return service.create(book, user_id=user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    service = BooksService(session)
    try:
        service.delete(book_id, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    service = BooksService(session)
    try:
        return service.update(book_id, book, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))