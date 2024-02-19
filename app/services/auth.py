from typing import Optional

from app.core.exceptions import HTTPUnauthenticatedException, HTTPUnauthorizedException
from tortoise.exceptions import DoesNotExist, IntegrityError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.schemas import UserCreate, UserResponse
from app.models import User
from app.schemas.token import TokenData
from app.core.sequrity import verify_password, get_password_hash, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:

    @staticmethod
    async def register_new_user(user: UserCreate) -> UserResponse:
        try:
            user_in_db = User(
                username=user.username,
                email=user.email,
                hashed_password=await get_password_hash(user.password)
            )
            await user_in_db.save()
            return UserResponse.from_orm(user_in_db)
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким username или email уже существует."
            )

    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[UserResponse]:
        try:
            user = await User.get(username=username)
        except DoesNotExist:
            raise HTTPUnauthenticatedException(
                status_code=400,
                detail="Неверное имя пользователя или пароль."
            )

        if not await verify_password(password, user.hashed_password):
            raise HTTPUnauthenticatedException(
                status_code=400,
                detail="Неверное имя пользователя или пароль."
            )

        return UserResponse.from_orm(user)

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
        credentials_exception = HTTPUnauthorizedException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            username = await decode_access_token(token)
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        return token_data
