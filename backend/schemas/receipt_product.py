from decimal import Decimal

from pydantic import BaseModel

from backend.schemas.payment import PaymentCreate


class ProductInput(BaseModel):
    name: str
    price: Decimal
    quantity: int


class ReceiptProductCreate(BaseModel):
    products: ProductInput
    payment: PaymentCreate


class ReceiptProductRead(ProductInput):
    total: Decimal
