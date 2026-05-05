from models import Profile
from repos.profiles import ProfilesRepository
from repos.user import UsersRepository
from schemas.user import ProfileBase, ProfileCreate


class ProfilesService:
    def __init__(self, profiles_repo: ProfilesRepository, users_repo: UsersRepository):
        self.profiles_repo = profiles_repo
        self.users_repo = users_repo

    def list(self) -> list[Profile]:
        return self.profiles_repo.list()

    def get_for_user(self, profile_id: int, user_id: int) -> Profile:
        profile = self.profiles_repo.get(profile_id)
        if not profile:
            raise LookupError("Profile not found")
        if profile.user_id != user_id:
            raise PermissionError("You do not have access to this profile")
        return profile

    def get(self, profile_id: int) -> Profile:
        profile = self.profiles_repo.get(profile_id)
        if not profile:
            raise LookupError("Profile not found")
        return profile

    def create(self, payload: ProfileCreate) -> Profile:
        user = self.users_repo.get(payload.user_id)
        if not user:
            raise LookupError("User not found")

        profile = Profile(**payload.model_dump(mode="json"))
        self.profiles_repo.add(profile)
        self.profiles_repo.commit()
        self.profiles_repo.refresh(profile)
        return profile

    def delete(self, profile_id: int) -> None:
        profile = self.profiles_repo.get(profile_id)
        if not profile:
            raise LookupError("Profile not found")

        self.profiles_repo.delete(profile)
        self.profiles_repo.commit()

    def update(self, profile_id: int, payload: ProfileBase, user_id: int) -> Profile:
        profile = self.profiles_repo.get(profile_id)
        if not profile:
            raise LookupError("Profile not found")

        if profile.user_id != user_id:
            raise PermissionError("You do not have access to this profile")

        data = payload.model_dump(mode="json", exclude_unset=True)
        for k, v in data.items():
            setattr(profile, k, v)

        self.profiles_repo.add(profile)
        self.profiles_repo.commit()
        self.profiles_repo.refresh(profile)
        return profile