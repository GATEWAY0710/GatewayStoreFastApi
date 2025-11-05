from abc import ABCMeta
from typing import List, Optional
from uuid import UUID
from domain.models import User


class UserRepository(metaclass=ABCMeta):
    """
        Default class for user repository implementation
    """

    def create(self, user: User) -> Optional[User]:
        """Create user"""
        raise NotImplementedError

    def create_admin(self, user: User) -> Optional[User]:
        """Create admin user"""
        raise NotImplementedError

    def update(self, user: User) -> Optional[User]:
        """Update user"""
        raise NotImplementedError

    def get(self, id: UUID) -> Optional[User]:
        """Get user by Id"""
        raise NotImplementedError

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        raise NotImplementedError

    def list(self) -> List[User]:
        """List user"""
        raise NotImplementedError