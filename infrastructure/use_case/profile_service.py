from logging import Logger
from typing import List, Optional
from uuid import UUID
from application.persistence.profile_repo import ProfileRepository
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.profile import CreateProfileResponse, Get, GetResponse, ListResponse, Update, \
    UpdateResponse
from application.use_case.profile_service import ProfileService as DefaultProfileService
from domain.models import Profile, User


class ProfileService(DefaultProfileService):
    _logger: Logger
    _profile_repository: ProfileRepository

    def __init__(self, logger: Logger, profile_repository: ProfileRepository):
        self._logger = logger
        self._profile_repository = profile_repository

    def create(self, user_id: str, profile: Profile) -> BaseResponse:
        self._logger.info(f"creating a profile with user id {user_id}")
        profile_exist = self._profile_repository.get(user_id=user_id)

        if profile_exist:
            self._logger.warning(f"profile with user id {user_id} already exist")
            response = BaseResponse(status=False, message=f"profile with user id {user_id} already exist")
            response._status_code = 400
            return response

        db_profile = Profile(user_id=user_id, first_name=profile.first_name, last_name=profile.last_name,
                             middle_name=profile.middle_name, phone_number=profile.phone_number)
        db_profile = self._profile_repository.create(db_profile)
        if not db_profile:
            self._logger.error(f"error occured while crioyuueating profile with user id {user_id}")
            response = BaseResponse(status=False,
                                    message=f"error occured while creating profile of user id {user_id}")
            response._status_code = 500
            return response

        self._logger.info(f"profile with user id {user_id} created succesfully")
        response = CreateProfileResponse(status=True, user_id=db_profile.user_id, first_name=db_profile.first_name,
                                         last_name=db_profile.last_name, middle_name=db_profile.middle_name)
        response._status_code = 200
        return response

    def update(self, user_id: str,  profile: Update) -> BaseResponse:
        profile_exist = self._profile_repository.get(user_id=user_id)
        if not profile_exist:
            self._logger.warning(f"profile with user id {user_id} does not exist")
            response = BaseResponse(status=False, message=f"profile with user id {user_id} does not exist")
            response._status_code = 400
            return response

        profile_exist.first_name = profile.first_name
        profile_exist.last_name = profile.last_name
        profile_exist.middle_name = profile.middle_name
        profile_exist.phone_number = profile.phone_number

        update_profile = self._profile_repository.update(user_id, profile_exist)
        if not update_profile:
            self._logger.error(f"error occured while updating profile with user id {user_id}")
            response = BaseResponse(status=False, message=f"error occured while updating profile of user id {user_id}")
            response._status_code = 500
            return response

        self._logger.info(f"profile with user id {user_id} updated succesfully")
        response = UpdateResponse(status=True, user_id=user_id, first_name=update_profile.first_name,
                                  last_name=update_profile.last_name, middle_name=update_profile.middle_name,
                                  phone_number=update_profile.phone_number)
        response._status_code = 200
        return response

    def get(self, user_id: UUID) -> BaseResponse:
        profile_exist = self._profile_repository.get(user_id=user_id)
        if not profile_exist:
            self._logger.warning(f"profile with user id {user_id} does not exist")
            response = BaseResponse(status=False, message=f"profile with user id {user_id} does not exist")
            response._status_code = 400
            return response

        self._logger.info(f"profile with user id {user_id} fetched successfully")
        response = GetResponse(status=True, user_id=user_id, first_name=profile_exist.first_name,
                               last_name=profile_exist.last_name,
                               phone_number=profile_exist.phone_number,
                               middle_name=profile_exist.middle_name)
        response._status_code = 200
        return response

    def list(self) -> BaseResponse:
        profiles = self._profile_repository.list()

        profile_responses = [
            CreateProfileResponse(status=True, **profile_dict)
            for profile_dict in profiles
        ]
        self._logger.info(f"list of profiles fetched")
        response = ListResponse(status=True, profiles=profile_responses)
        return response
