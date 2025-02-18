from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from backend.authentication.utils import hash_password
from backend.config import settings
from backend.config.exceptions.user import UsersException
from backend.models import User
from backend.repositories import UserRepository
from backend.routers.dependencies import get_user_repository
from backend.schemas.user import UserCreate

router = APIRouter(
    prefix=settings.api_prefix.auth,
    tags=["Auth"],
)


@router.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@router.post(
    "/registration",
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
