from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from api.token import allowed_roles, get_current_user
from application.use_case.models.auth import TokenData
from application.use_case.models.profile import CreateProfile, CreateProfileResponse, Get, GetResponse, ListResponse, Update, UpdateResponse
from infrastructure.dependency import Container

oauth2_token = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("", response_model=CreateProfileResponse)
def create(profile: CreateProfile ,current_user: TokenData = Depends(get_current_user)):
    profile_service = Container.profile_service()
    response = profile_service.create(user_id=current_user.user_id, profile=profile)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.put("/{update}", response_model=UpdateResponse)
def update(profile: Update, current_user: TokenData = Depends(get_current_user)):
    profile_service = Container.profile_service()
    response = profile_service.update(current_user.user_id, profile=profile)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/{id}", response_model=GetResponse)
def get(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin", "Customer"]))]):
    profile_service = Container.profile_service()
    response = profile_service.get(user_id=current_user.user_id)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response


@router.get("", response_model=ListResponse)
def list(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    profile_service = Container.profile_service()
    response = profile_service.list()
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response