from typing import TYPE_CHECKING

from fastapi import Depends, Header, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from backend.authentication.strategies import decode_jwt
from backend.config.exceptions import UsersException
from backend.database import db_helper
from backend.repositories import UserRepository
from backend.repositories.receipt import ReceiptRepository
from backend.schemas.user import UserRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> UserRepository:
    return UserRepository(session=session)


async def get_receipt_repository(
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> ReceiptRepository:
    return ReceiptRepository(session=session)


async def validate_auth_user(
    user_repo: UserRepository = Depends(get_user_repository),
    token: str = Header(alias="x-auth-token"),
) -> UserRead:
    try:
        check_user = decode_jwt(token=token)
        if not check_user:
            pass
        user = await user_repo.get_by_id(int(check_user["sub"]))
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=UsersException.unauthorized,
        )

    return user
