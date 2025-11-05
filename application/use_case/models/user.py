from typing import List, Optional
from pydantic import BaseModel, EmailStr, UUID4

from application.use_case.models.base_response import BaseResponse

class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str


    def validate_password(self):
        return self.password == self.confirm_password


class UserResponse(BaseResponse):
    id: UUID4
    email: EmailStr
    username: str
    role: str

class Get(BaseModel):
    id: str

class GetResponse(BaseResponse):
    id: UUID4
    email: EmailStr
    username: str
    role: str

class ListUsers(BaseResponse):
    users: List[UserResponse]