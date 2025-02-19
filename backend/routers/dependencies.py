from typing import TYPE_CHECKING

from fastapi import Depends, Header

from backend.authentication.strategies import decode_jwt
from backend.database import db_helper
from backend.models import User
from backend.repositories import UserRepository
from backend.schemas.user import UserRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> UserRepository:
    return UserRepository(session=session)


async def validate_auth_user(
    user_repo: UserRepository = Depends(get_user_repository),
    token: str = Header(alias="x-auth-token"),
) -> UserRead:
    check_user = decode_jwt(token=token)
    if not check_user:
        pass

    user = await user_repo.get_by_id(int(check_user["sub"]))

    return user
