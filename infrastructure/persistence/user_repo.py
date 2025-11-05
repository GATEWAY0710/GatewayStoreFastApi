from datetime import timedelta
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select
from domain.enums import role
from application.persistence.user_repo import UserRepository as DefaultUserRepository
from domain.models import User
from infrastructure.database import SessionLocal
from logging import Logger

class UserRepository(DefaultUserRepository):
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger


    def create(self, user: User) -> Optional[User]:
        with SessionLocal() as session:
            try:
                session.add(user)
                self._logger.info(f"Created new user {user.id}")
                session.commit()
                session.refresh(user)
                return user
            except Exception as e:
                self._logger.error(f"Failed to create new user {user.id}: {e}")
                return None

    def create_admin(self, user: User) -> Optional[User]:
        with SessionLocal() as session:
            try:
                session.add(user)
                self._logger.info(f"Created new admin {user.id}")
                session.commit()
                session.refresh(user)
                return user
            except Exception as e:
                self._logger.error(f"Failed to create new admin {user.id}: {e}")
                return None


    def update(self, user: User) -> Optional[User]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(User).where(User.id == user.id)
                )
                db_user = session.scalars(statement).one_or_none()
                if db_user is None:
                    self._logger.info(f"User {user.id} does not exist")
                    return None
                db_user.id = user.id
                db_user.username = user.username
                db_user.created_at = user.created_at
                db_user.modified_at = user.modified_at
                db_user.created_by = user.created_by
                db_user.modified_by = user.modified_by
                session.commit()
                session.refresh(db_user)
                return db_user
            except Exception as e:
                self._logger.error(f"Failed to update user {user.id}: {e}")
                return None

    def get(self, id: UUID) -> Optional[User]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(User).where(User.id == str(id))
                )
                user = session.scalars(statement).one_or_none()
                return user
            except Exception as e:
                self._logger.error(f"Failed to get user {id}: {e}")
                return None

    def get_by_email(self, email: str) -> Optional[User]:
        with SessionLocal() as session:
            try:
                statement = (
                    select(User).where(User.email == email)
                )
                user = session.scalars(statement).one_or_none()
                return user
            except Exception as e:
                self._logger.error(f"Failed to get user {email}: {e}")
                return None

    def list(self)-> List[User]:
        with SessionLocal() as session:
            db_users = session.scalars(select(User)).all()
            users = []
            for db_user in db_users:
                users.append(db_user)
            return users
