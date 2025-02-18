from typing import TYPE_CHECKING

from fastapi import Depends

from backend.database import db_helper
from backend.repositories import UserRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def get_user_repository(
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> UserRepository:
    return UserRepository(session=session)
