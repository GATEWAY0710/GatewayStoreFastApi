from uuid import UUID
import uuid
from logging import Logger
from domain.enums.role import Role

from application.use_case.models.base_response import BaseResponse
from application.use_case.models.user import CreateUser, UserResponse, GetResponse, ListUsers
from application.use_case.user_service import UserService as DefaultUserService
from domain.models import User
from infrastructure.hashing import HashingService
from infrastructure.persistence.user_repo import UserRepository

class UserService(DefaultUserService):
    _logger: Logger
    _user_repo: UserRepository

    def __init__(self, logger: Logger, user_repo: UserRepository):
        self._logger = logger
        self._user_repo = user_repo

    def create_admin(self, user:CreateUser)-> BaseResponse:
        self._logger.info(f"Creating new user {user.email}")

        existing_user = self._user_repo.get_by_email(email=user.email)
        if existing_user:
            self._logger.warning(f"User {user.email} already exists")
            response = BaseResponse(status=False, message="User already exists")
            response._status_code = "400"
            return response

        if not user.validate_password():
            self._logger.warning(f"Password is invalid for user {user.email}")
            response = BaseResponse(status=False, message="Password is invalid")
            response._status_code = "400"
            return response

        hash_salt, password_hash = HashingService().hash_password(user.password)
        if user.username is None:
            user.username = str(user.email)

        user = User(
            id=uuid.uuid4(),
            email=str(user.email),
            username=user.username,
            password_hash=password_hash,
            hash_salt=hash_salt,
            role=Role.Admin
        )
        user = self._user_repo.create_admin(user)
        if not user:
            self._logger.error(f"Failed to create new user")
            response = BaseResponse(status=False, message="Failed to create new user")
            response._status_code = "500"
            return response
        self._logger.info(f"Created new user {user.email}")
        response = UserResponse(status=True, message="User created successfully", id=user.id, email=str(user.email), role=user.role.value, username=user.username)
        response._status_code = "201"
        return response


    def create(self, user:CreateUser)-> BaseResponse:
        self._logger.info(f"Creating new user {user.email}")

        existing_user = self._user_repo.get_by_email(email=user.email)
        if existing_user:
            self._logger.warning(f"User {user.email} already exists")
            response = BaseResponse(status=False, message="User already exists")
            response._status_code = "400"
            return response

        if not user.validate_password():
            self._logger.warning(f"Password is invalid for user {user.email}")
            response = BaseResponse(status=False, message="Password is invalid")
            response._status_code = "400"
            return response

        hash_salt, password_hash = HashingService().hash_password(user.password)
        if user.username is None:
            user.username = str(user.email)

        user = User(
            id=uuid.uuid4(),
            email=str(user.email),
            username=user.username,
            password_hash=password_hash,
            hash_salt=hash_salt,
            role=Role.Customer
        )
        user = self._user_repo.create_admin(user)
        if not user:
            self._logger.error(f"Failed to create new user")
            response = BaseResponse(status=False, message="Failed to create new user")
            response._status_code = "500"
            return response
        self._logger.info(f"Created new user {user.email}")
        response = UserResponse(status=True, message="User created successfully", id=user.id, email=str(user.email), role=user.role.value, username=user.username)
        response._status_code = "201"
        return response


    def get(self, id: UUID) -> BaseResponse:
        user_exist = self._user_repo.get(id=id)
        if not user_exist:
            self._logger.warning(f"User {id} does not exist")
            response = BaseResponse(status=False, message="User does not exist")
            response._status_code = "400"
            return response
        self._logger.info(f"Getting user {id}")
        response = GetResponse(status=True, message="User retrieved successfully", id=user_exist.id, email=str(user_exist.email), role=user_exist.role.value, username=user_exist.username)
        response._status_code = "200"
        return response


    def get_by_email(self, email: str) -> BaseResponse:
        user_exist = self._user_repo.get_by_email(email=email)
        if not user_exist:
            self._logger.warning("User does not exist")
            response = BaseResponse(status=False, message="User does not exist")
            response._status_code = "400"
            return response
        self._logger.info(f"Getting user {email}")
        response = GetResponse(status=True, message="User retrieved successfully", id=user_exist.id, email=str(user_exist.email), role=user_exist.role.value, username=user_exist.username)
        response._status_code = "200"
        return response


    def list(self) -> BaseResponse:
        users = self._user_repo.list()
        user_responses = []
        for user in users:
            user_response = UserResponse(status=True, id=user.id, email=user.email, username=user.username, role=user.role.value)
            user_responses.append(user_response)

        self._logger.info(f"list of users fetched")
        response = ListUsers(status=True, users=user_responses)
        response._status_code = "200"
        return response

    def authenticate(self, email, password):
        user = self._user_repo.get_by_email(email=email)
        if not user:
            response = BaseResponse(status=False, message="Invalid email or password")
            response._status_code = "401"
            return response

        if not HashingService().validate_password(password, user.password_hash, user.hash_salt):
            response = BaseResponse(status=False, message="Invalid email or password")
            response._status_code = "401"
            return response

        return BaseResponse(status=True, message="User authenticated successfully")