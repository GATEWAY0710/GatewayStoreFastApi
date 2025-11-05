from pydantic import BaseModel
from application.use_case.models.auth import TokenResponse
from fastapi import APIRouter, Depends, HTTPException, status, Body
from application.use_case.models.user import UserResponse, GetResponse
from infrastructure.dependency import Container
from api.token import create_token


class TokenRequest(BaseModel):
    email: str
    password: str


router = APIRouter()


@router.post("/token", response_model=TokenResponse)
def token(tokenRequest: TokenRequest = Body(...)):
    user_service = Container.user_service()
    response = user_service.authenticate(tokenRequest.email, tokenRequest.password)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)

    response: UserResponse = Container.user_service().get_by_email(tokenRequest.email)

    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)

    email = response.email
    user_id = response.id
    username = response.username
    role = response.role

    data = {
        "sub": email,
        "user_id": str(user_id),
        "username": username,
        "roles": [role]
    }

    access_token, refresh_token, expire = create_token(data, expires_delta=None)

    return TokenResponse(
        status=True,
        message="Token generated successfully",
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=int(expire.timestamp())
    )