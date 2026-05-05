from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.auth import AuthManager
from connection import get_session
from models import User
from repos.profiles import ProfilesRepository
from repos.user import UsersRepository
from schemas.user import (
    ProfileBase,
    ProfileCreate,
    ProfileResponse,
    UserBase,
    UserDetailResponse,
    UserResponse,
    UserUpdate, UserLogin, TokenResponse, ChangePasswordRequest,
)
from services.profiles import ProfilesService
from services.users import UsersService

router = APIRouter(tags=["users"])
auth_manager = AuthManager()

# Profiles

# @router.get("/profiles", response_model=list[ProfileResponse])
# def profile_list(session: Session = Depends(get_session)):
#     profiles_service = ProfilesService(
#         profiles_repo=ProfilesRepository(session),
#         users_repo=UsersRepository(session),
#     )
#     return profiles_service.list()


@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):

    profiles_service = ProfilesService(
        profiles_repo=ProfilesRepository(session),
        users_repo=UsersRepository(session),
    )
    try:
        return profiles_service.get_for_user(profile_id=profile_id, user_id=user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/profiles", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(payload: ProfileCreate, session: Session = Depends(get_session)):
    profiles_service = ProfilesService(
        profiles_repo=ProfilesRepository(session),
        users_repo=UsersRepository(session),
    )
    try:
        return profiles_service.create(payload)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, session: Session = Depends(get_session),
                   user=Depends(auth_manager.auth_wrapper)):
    profiles_service = ProfilesService(
        profiles_repo=ProfilesRepository(session),
        users_repo=UsersRepository(session),
    )
    try:
        profiles_service.delete(profile_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/profiles/{profile_id}", response_model=ProfileResponse)
def update_profile(profile_id: int, payload: ProfileBase, session: Session = Depends(get_session),
                   user: User=Depends(auth_manager.get_current_user)):
    profiles_service = ProfilesService(
        profiles_repo=ProfilesRepository(session),
        users_repo=UsersRepository(session),
    )
    try:
        return profiles_service.update(profile_id, payload, user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Users

@router.get("/users", response_model=list[UserResponse])
def user_list(session: Session = Depends(get_session)):
    users_service = UsersService(users_repo=UsersRepository(session))
    return users_service.list()


@router.get("/users/me", response_model=UserDetailResponse)
def user_me(session: Session = Depends(get_session), user: User=Depends(auth_manager.get_current_user)):
    return user


# @router.get("/users/{user_id}", response_model=UserDetailResponse)
# def get_user(user_id: int, session: Session = Depends(get_session), user=Depends(auth_manager.auth_wrapper)):
#     users_service = UsersService(users_repo=UsersRepository(session))
#     try:
#         return users_service.get_detail(user_id)
#     except LookupError as e:
#         raise HTTPException(status_code=404, detail=str(e))


@router.post("/registration", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase, session: Session = Depends(get_session)):
    users_service = UsersService(users_repo=UsersRepository(session))
    try:
        return users_service.create(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    users_service = UsersService(users_repo=UsersRepository(session))
    try:
        token = users_service.login(user)
        return TokenResponse(access_token=token)
    except LookupError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")


@router.delete("/users/delete", status_code=status.HTTP_204_NO_CONTENT)
def user_delete(session: Session = Depends(get_session), user=Depends(auth_manager.auth_wrapper)):
    users_service = UsersService(users_repo=UsersRepository(session))
    try:
        users_service.delete(user.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/users/update", response_model=UserResponse)
def update_user(payload: UserUpdate, session: Session = Depends(get_session),
                user: User=Depends(auth_manager.get_current_user)):
    users_service = UsersService(users_repo=UsersRepository(session))
    try:
        return users_service.update(user.id, payload)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/users/change_password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(payload: ChangePasswordRequest, session: Session = Depends(get_session),
            user: User = Depends(auth_manager.get_current_user)):

    users_service = UsersService(users_repo=UsersRepository(session))
    try:
        users_service.change_password(user_id=user.id, payload=payload)
        return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))