from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from application.use_case.models.auth import TokenData
from api.token import get_current_user, allowed_roles
from infrastructure.dependency import Container
from application.use_case.models.user import CreateUser, GetResponse, UserResponse, ListUsers

oauth2_token = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("{admin}", response_model=UserResponse)
def create_admin(request: CreateUser, current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    user_service = Container.user_service()
    response = user_service.create_admin(request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.post("", response_model=UserResponse)
def create(request: CreateUser):
    user_service = Container.user_service()
    response = user_service.create(request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response


@router.get("/filter", response_model=GetResponse)
def get_by_email(current_user: TokenData = Depends(get_current_user)):
    user_service = Container.user_service()
    response = user_service.get_by_email(current_user.email)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response





@router.get("/user", response_model=GetResponse)
def get(current_user: TokenData = Depends(get_current_user)):
    user_service = Container.user_service()
    response = user_service.get(current_user.user_id)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response





@router.get("", response_model=ListUsers)
def list(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    email = current_user.email
    user_service = Container.user_service()
    response = user_service.list()
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response