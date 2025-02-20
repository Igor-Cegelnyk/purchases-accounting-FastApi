from typing import Any
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from backend.models import Receipt, ReceiptProduct, Payment
from backend.repositories import SqlAlchemyRepository


class ReceiptRepository(SqlAlchemyRepository):
    model = Receipt

    async def create(self, instance: Receipt) -> Receipt:
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get_receipts(
        self,
        receipt_id: int | None = None,
        user_id: int | None = None,
        receipt_cost: float | None = None,
        payment_type: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, dict[str, Any] | list[dict[str, Any]] | Any]]:
        stmt = (
            select(Receipt)
            .options(
                selectinload(Receipt.products).joinedload(ReceiptProduct.product),
                joinedload(Receipt.payment),
                joinedload(Receipt.user),
            )
            .order_by(Receipt.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        if user_id:
            stmt = stmt.where(Receipt.user_id == user_id)

        if date_from:
            stmt = stmt.where(Receipt.created_at >= date_from)

        if date_to:
            stmt = stmt.where(Receipt.created_at <= date_to)

        if receipt_id:
            stmt = stmt.where(Receipt.id == receipt_id)

        if receipt_cost:
            stmt = stmt.where(Receipt.total >= receipt_cost)

        if payment_type:
            stmt = stmt.join(Receipt.payment, isouter=False).where(
                Payment.type == payment_type
            )

        result = await self.session.execute(stmt)
        receipts = result.scalars().all()

        return [
            {
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
                "total": receipt.total,
                "rest": receipt.payment.amount - receipt.total,
                "created_at": receipt.created_at.astimezone(
                    ZoneInfo("Europe/Kyiv")
                ).isoformat(),
            }
            for receipt in receipts
        ]
