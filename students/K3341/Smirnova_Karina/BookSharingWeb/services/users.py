from auth.auth import AuthManager
from models import User
from repos.user import UsersRepository
from schemas.user import UserBase, UserUpdate, UserLogin, ChangePasswordRequest

auth_manager = AuthManager()


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    def list(self) -> list[User]:
        return self.users_repo.list()

    def get_detail(self, user_id: int) -> User:
        user = self.users_repo.get_detail(user_id)
        if not user:
            raise LookupError("User not found")
        return user

    def create(self, inuser: UserBase) -> User:
        existing = self.users_repo.get_by_email(inuser.email)
        if existing:
            raise ValueError("Email already registered")

        user = User(username=inuser.username, email=inuser.email,
                    password=auth_manager.get_password_hash(inuser.password))
        self.users_repo.add(user)
        self.users_repo.commit()
        self.users_repo.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        user = self.users_repo.get(user_id)
        if not user:
            raise LookupError("User not found")

        self.users_repo.delete(user)
        self.users_repo.commit()

    def update(self, user_id: int, payload: UserUpdate) -> User:
        user = self.users_repo.get(user_id)
        if not user:
            raise LookupError("User not found")

        data = payload.model_dump(mode="json", exclude_unset=True)

        if "email" in data and data["email"] != user.email:
            existing = self.users_repo.get_by_email(data["email"])
            if existing:
                raise ValueError("Email already registered")

        for k, v in data.items():
            setattr(user, k, v)

        self.users_repo.add(user)
        self.users_repo.commit()
        self.users_repo.refresh(user)
        return user

    def login(self, payload: UserLogin) -> str:
        user = self.users_repo.get_by_email(payload.email)
        if not user:
            raise LookupError("Invalid credentials")

        if not auth_manager.verify_password(payload.password, user.password):
            raise LookupError("Invalid credentials")

        token = auth_manager.encode_token(user.email)
        return token

    def change_password(self, user_id: int, payload: ChangePasswordRequest) -> User:
        db_user = self.users_repo.get(user_id)
        if not db_user:
            raise LookupError("User not found")

        if not auth_manager.verify_password(payload.old_password, db_user.password):
            raise ValueError("Old password is incorrect")

        db_user.password = auth_manager.get_password_hash(payload.new_password)

        self.users_repo.add(db_user)
        self.users_repo.commit()
        self.users_repo.refresh(db_user)
        return db_user