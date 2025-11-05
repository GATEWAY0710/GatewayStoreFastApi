from datetime import timedelta, datetime, timezone
from typing import Annotated, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from infrastructure.dependency import Container
import logging
from application.use_case.models.auth import TokenData
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(data: dict, expires_delta: Union[timedelta, None] = None) -> tuple[str, str, datetime] :
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    refresh_exp = expire + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = refresh_exp
    encoded_refresh_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, encoded_refresh_jwt, expire

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(
            email=email,
            user_id=payload.get("user_id"),
            username=payload.get("username"),
            roles=payload.get("roles", [])
        )
    except InvalidTokenError:
        raise credentials_exception
    user = Container.user_service().get_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return token_data

def allowed_roles(required_roles: list[str]):
    def role_checker(current_user: Annotated[TokenData, Depends(get_current_user)]):
        if required_roles == []:
            return current_user
        if not any(role in current_user.roles for role in required_roles):
            logging.warning(f"User with roles {current_user.roles} tried to access a resource requiring roles {required_roles}")
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
    return role_checker
