from pydantic import BaseModel
from application.use_case.models.base_response import BaseResponse


class TokenResponse(BaseResponse):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    email: str
    user_id: str
    username: str
    roles: list[str]