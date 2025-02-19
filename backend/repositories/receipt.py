from typing import Annotated
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from backend.models import Receipt, ReceiptProduct
from backend.repositories import SqlAlchemyRepository


class ReceiptRepository(SqlAlchemyRepository):
    model = Receipt

    async def create(self, instance: Receipt) -> Receipt:
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get_by_id(self, id: int) -> Annotated[dict, None]:
        stmt = (
            select(Receipt)
            .where(Receipt.id == id)
            .options(
                selectinload(Receipt.products).joinedload(ReceiptProduct.product),
                joinedload(Receipt.payment),
                joinedload(Receipt.user),
            )
        )

        result = await self.session.execute(stmt)
        receipt = result.scalars().first()

        if not receipt:
            return None

        return {
            "id": receipt.id,
            "products": [
                {
                    "name": rp.product.name,
                    "price": rp.price,
                    "quantity": rp.quantity,
                    "total": rp.total,
                }
                for rp in receipt.products
            ],
            "payment": {
                "type": receipt.payment.type.value,
                "amount": receipt.payment.amount,
            },
            "total": sum(rp.total for rp in receipt.products),
            "rest": receipt.payment.amount - sum(rp.total for rp in receipt.products),
            "created_at": receipt.created_at.replace(tzinfo=ZoneInfo("UTC"))
            .astimezone(ZoneInfo("Europe/Kyiv"))
            .isoformat(),
        }
