from abc import ABCMeta
from uuid import UUID

from application.use_case.models.base_response import BaseResponse
from application.use_case.models.profile import CreateProfile, Update


class ProfileService(metaclass=ABCMeta):
    """Default class for profile service implementation"""

    def create(self, user_id: str, profile: CreateProfile) -> BaseResponse:
        """create profile"""
        raise NotImplementedError

    def update(self, profile: Update) -> BaseResponse:
        """update profile"""
        raise NotImplementedError

    def get(self, user_id: UUID) -> BaseResponse:
        """get profile"""
        raise NotImplementedError

    def list(self) -> BaseResponse:
        """list profiles"""
        raise NotImplementedError