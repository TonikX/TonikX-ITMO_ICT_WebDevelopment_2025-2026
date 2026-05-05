from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.auth import AuthManager
from connection import get_session
from models import User
from schemas.chat import (
    ChatBase,
    ChatCreate,
    ChatResponse,
    MessageBase,
    MessageCreate,
    MessageResponse,
)
from schemas.deal import DealDetailResponse
from services.chats import ChatsService

router = APIRouter(tags=["chat"])
auth_manager = AuthManager()



@router.get("/chats", response_model=list[ChatResponse])
def chat_list(session: Session = Depends(get_session)):
    return ChatsService(session).list_chats()


@router.get("/chats/{chat_id}", response_model=ChatResponse)
def chat_by_id(chat_id: int, session: Session = Depends(get_session),
               user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).get_chat(chat_id, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/chats", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(payload: ChatCreate, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).create_chat(payload, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/chats/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    try:
        ChatsService(session).delete_chat(chat_id, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.patch("/chats/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: int, payload: ChatBase, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).update_chat(chat_id, payload, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))



@router.get("/chats/{chat_id}/messages", response_model=list[MessageResponse])
def message_list(chat_id: int, session: Session = Depends(get_session),
                 user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).list_messages(chat_id, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/messages/{message_id}", response_model=MessageResponse)
def message_by_id(message_id: int, session: Session = Depends(get_session),
                  user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).get_message(message_id, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(payload: MessageCreate, session: Session = Depends(get_session),
                   user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).create_message(payload, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(message_id: int, session: Session = Depends(get_session),
                   user: User=Depends(auth_manager.get_current_user)):
    try:
        ChatsService(session).delete_message(message_id, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.patch("/messages/{message_id}", response_model=MessageResponse)
def update_message(message_id: int, payload: MessageBase, session: Session = Depends(get_session),
                   user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).update_message(message_id, payload, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))



@router.get("/users/chats", response_model=list[ChatResponse])
def user_chats(session: Session = Depends(get_session),
               user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).list_user_chats(user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/deals", response_model=list[DealDetailResponse])
def user_deals(session: Session = Depends(get_session),
               user: User=Depends(auth_manager.get_current_user)):
    try:
        return ChatsService(session).list_user_deals(user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))