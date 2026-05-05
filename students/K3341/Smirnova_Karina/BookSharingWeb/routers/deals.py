from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.auth import AuthManager
from connection import get_session
from models import User
from schemas.deal import DealCreate, DealDetailResponse, DealResponse, DealUpdate
from services.deals import DealsService

router = APIRouter(prefix="/deals", tags=["deals"])
auth_manager = AuthManager()



@router.get("/", response_model=list[DealResponse])
def deal_list(session: Session = Depends(get_session)):
    service = DealsService(session)
    return service.list()


@router.get("/{deal_id}", response_model=DealDetailResponse)
def deal_by_id(deal_id: int, session: Session = Depends(get_session),
               user: User=Depends(auth_manager.get_current_user)):
    service = DealsService(session)
    try:
        return service.get_detail(deal_id, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
def create_deal(payload: DealCreate, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    service = DealsService(session)
    try:
        return service.create(payload, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deal(deal_id: int, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    service = DealsService(session)
    try:
        service.delete(deal_id, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{deal_id}", response_model=DealResponse)
def update_deal(deal_id: int, payload: DealUpdate, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    service = DealsService(session)
    try:
        return service.update(deal_id, payload, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))