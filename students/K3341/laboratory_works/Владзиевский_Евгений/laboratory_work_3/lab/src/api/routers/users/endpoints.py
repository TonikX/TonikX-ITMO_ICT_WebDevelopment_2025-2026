from fastapi import APIRouter, Depends

from src.api.routers.users import models
from src.api.security import access_policy
from src.api.sessions import get_db_session
from src.db.crud import get_user_by_id, update_user

router = APIRouter(
    prefix='/user',
    tags=["users"],
    dependencies=[Depends(access_policy)]
)


@router.get("/{id:int}", response_model=models.UserResponse)
async def get_user(id: int, session=Depends(get_db_session)):
    user = await get_user_by_id(session, id)
    return user


@router.get("/me", response_model=models.UserResponse)
async def get_me(credentials=Depends(access_policy), session=Depends(get_db_session)):
    user = await get_user_by_id(session, credentials.subject['id'])
    return user


@router.post("/edit", response_model=models.UserResponse)
async def edit_user(form: models.UserEdit, session=Depends(get_db_session), credentials=Depends(access_policy)):
    return await update_user(session, credentials.subject['id'], name=form.name, about=form.about,
                             img_hash=form.img_hash)
