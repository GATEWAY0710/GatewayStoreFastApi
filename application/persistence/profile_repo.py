from abc import ABCMeta
from typing import List, Optional
from uuid import UUID

from domain.models import Profile


class ProfileRepository(metaclass=ABCMeta):
    """
        default class for profile repository
    """

    def create(self, profile: Profile) -> Optional[Profile]:
        """create profile"""
        raise NotImplementedError

    def update(self, profile: Profile) -> Optional[Profile]:
        """update a profile"""
        raise NotImplementedError

    def get(self, user_id: UUID) -> Optional[Profile]:
        """get a profile"""
        raise NotImplementedError

    def list(self) -> List[Profile]:
        """list profiles"""
        raise NotImplementedError