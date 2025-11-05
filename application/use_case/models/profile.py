from typing import List, Optional
from pydantic import UUID4, BaseModel

from application.use_case.models.base_response import BaseResponse


class CreateProfile(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    phone_number: str


class CreateProfileResponse(BaseResponse):
    user_id: UUID4
    first_name: str
    last_name: str
    middle_name: Optional[str] = None


class Get(BaseModel):
    user_id: str


class GetResponse(BaseResponse):
    user_id: UUID4
    first_name: str
    last_name: str
    phone_number: str
    middle_name: Optional[str]



class Update(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    phone_number: str


class UpdateResponse(BaseResponse):
    user_id: UUID4
    first_name: str
    last_name: str
    phone_number: str
    middle_name: Optional[str] = None


class ListResponse(BaseResponse):
    profiles: List[CreateProfileResponse]