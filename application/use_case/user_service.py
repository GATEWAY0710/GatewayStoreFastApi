from abc import ABCMeta
from uuid import UUID
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.user import CreateUser


class UserService(metaclass=ABCMeta):
    """
        Default class for user service implementation
    """

    def create(self, user: CreateUser) -> BaseResponse:
        """Create user"""
        raise NotImplementedError

    def create_admin(self, user: CreateUser) -> BaseResponse:
        """Create admin user"""
        raise NotImplementedError

    def get(self, id: UUID) -> BaseResponse:
        """Get user by Id"""
        raise NotImplementedError

    def get_by_email(self, email: str) -> BaseResponse:
        """Get user by email"""
        raise NotImplementedError

    def list(self) -> BaseResponse:
        """List user"""
        raise NotImplementedError