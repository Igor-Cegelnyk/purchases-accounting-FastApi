from fastapi import APIRouter, Depends, HTTPException, Header, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from typing_extensions import Annotated

from backend.authentication.strategies import encode_jwt
from backend.authentication.utils import hash_password, validate_password
from backend.config import settings
from backend.config.exceptions import UsersException
from backend.models import User
from backend.repositories import UserRepository
from backend.routers.dependencies import get_user_repository
from backend.schemas.user import UserCreate

router = APIRouter(
    prefix=settings.api_prefix.auth,
    tags=["Auth"],
)


@router.post(
    "/registration",
    summary="Реєстрація користувача",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": UsersException.registration_successful},
        400: {"description": UsersException.already_exist},
        422: {
            "description": f"'{UsersException.invalid_password}', "
            f"або '{UsersException.invalid_first_name}',"
            f"або '{UsersException.invalid_username}'"
        },
    },
)
async def user_registration(
    user_in: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository),
):
    hashed_password = hash_password(password=str(user_in.password))

    try:
        await user_repo.create(
            User(
                first_name=user_in.first_name,
                username=user_in.username,
                password=hashed_password,
            )
        )
    except IntegrityError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=UsersException.already_exist,
        )

    return UsersException.registration_successful


@router.post(
    "/login",
    summary="Автентифікація зареєстрованого користувача",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Повертається згенерований jwt"},
        401: {"description": UsersException.bad_login},
    },
)
async def auth_user(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: UserRepository = Depends(get_user_repository),
):
    user = await user_repo.get_user_by_username(form_data.username)
    check_password = validate_password(
        password=form_data.password, hashed_password=user.password
    )
    if not user or not check_password or not user.active:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=UsersException.bad_login,
        )
    access_token = encode_jwt(payload={"sub": str(user.id), "username": user.username})
    response.headers["x-auth-token"] = f"Bearer {access_token}"
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
