from sqlmodel import Session, select

from models import Profile


class ProfilesRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> list[Profile]:
        return self.session.exec(select(Profile)).all()

    def get(self, profile_id: int) -> Profile | None:
        return self.session.get(Profile, profile_id)

    def add(self, profile: Profile) -> Profile:
        self.session.add(profile)
        return profile

    def delete(self, profile: Profile) -> None:
        self.session.delete(profile)

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, profile: Profile) -> None:
        self.session.refresh(profile)