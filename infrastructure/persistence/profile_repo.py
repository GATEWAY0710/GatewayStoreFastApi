from logging import Logger
from typing import List, Optional
from uuid import UUID
from domain.models import Profile
from infrastructure.database import SessionLocal
from sqlalchemy import select
from application.persistence.profile_repo import ProfileRepository as DefaultprofileRepository


class ProfileRepository(DefaultprofileRepository):
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger

    def create(self, profile: Profile) -> Optional[Profile]:
        with SessionLocal() as session:
            try:
                session.add(profile)
                self._logger.info(f"profile with id {profile.id} created succesfully")
                session.commit()
                session.refresh(profile)
                return profile
            except Exception as e:
                self._logger.error(f"an error occured while creating profile, {e}")
                return None

    def update(self, user_id: UUID, profile: Profile) -> Optional[Profile]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(Profile)
                    .where(Profile.user_id == user_id)
                )
                update = session.scalars(statement).one_or_none()

                if not update:
                    return None
                update.first_name = profile.first_name
                update.last_name = profile.last_name
                update.middle_name = profile.middle_name
                update.phone_number = profile.phone_number

                session.commit()
                session.refresh(update)
                return update
            except Exception as e:
                self._logger.error(f"unable to update profile with id{user_id}")
                return None

    def get(self, user_id: UUID) -> Optional[Profile]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(Profile).where(Profile.user_id == str(user_id))
                )
                profile = session.scalars(statement).one_or_none()
                return profile
            except Exception as e:
                self._logger.error(f"unable to get profile with user id {user_id}, {e}")
                return None

    def list(self) -> List[Profile]:
        with SessionLocal() as session:
            profiles = session.scalars(select(Profile)).all()
            return [
                {"user_id": u.user_id, "first_name": u.first_name, "last_name": u.last_name,
                 "middle_name": u.middle_name, "phone_number": u.phone_number}
                for u in profiles
            ]