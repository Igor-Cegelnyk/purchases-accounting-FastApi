from typing import Annotated

from sqlalchemy import select

from backend.models import User
from backend.repositories import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def get_user_by_username(self, username: str) -> Annotated[User, None]:
        stmt = select(self.model).filter_by(username=username)
        result = await self.session.scalar(stmt)
        return result
