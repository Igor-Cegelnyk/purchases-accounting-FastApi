from typing import TypeVar, TYPE_CHECKING, Annotated, Any

from sqlalchemy import select, Sequence, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)


class SqlAlchemyRepository:
    model = None

    def __init__(self, session: "AsyncSession"):
        self.session = session

    async def create(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(
        self,
        instance: ModelType,
        instance_update: dict,
    ) -> ModelType:
        for name, value in instance_update.items():
            setattr(instance, name, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)
        await self.session.commit()

    async def get_by_id(self, id: int) -> Annotated[ModelType, None]:
        stmt = select(self.model).filter_by(id=id)
        result = await self.session.scalar(stmt)
        return result

    async def get_all(
        self,
        filters: dict = None,
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        stmt = select(self.model).order_by("id")
        if filters:
            stmt = stmt.filter_by(**filters)
        result = await self.session.scalars(stmt)
        return result.all()
