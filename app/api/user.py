from datetime import timedelta

from app.core.exceptions import HTTPUnauthenticatedException
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.models import User
from app.core.sequrity import create_access_token
from app.services import auth_service
from app.schemas import UserCreate, UserResponse, Token, TokenData
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_create: UserCreate):

    """ Регистрация пользователя """

    user = await auth_service.register_new_user(user_create)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при регистрации пользователя."
        )
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    """ Авторизация пользователя """

    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPUnauthenticatedException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные."
        )
    access_token = await create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token}


@router.get("/users/me", response_model=UserResponse)
async def users_me(current_user: TokenData = Depends(auth_service.get_current_user)):

    """ Получение информации о текущем пользователе """

    user = await User.get(username=current_user.username)
    return UserResponse.from_orm(user)
