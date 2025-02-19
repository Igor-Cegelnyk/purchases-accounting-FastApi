from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from backend.schemas.payment import PaymentCreate
from backend.schemas.receipt_product import ProductInput


class ReceiptCreate(BaseModel):
    products: list[ProductInput]
    payment: PaymentCreate


class ReceiptRead(ReceiptCreate):
    id: int
    created_at: datetime
    total: Decimal
    rest: Decimal
