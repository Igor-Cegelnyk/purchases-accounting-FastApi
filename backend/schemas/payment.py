from decimal import Decimal

from pydantic import BaseModel

from backend.models import PaymentTypeEnum


class PaymentBase(BaseModel):
    type: PaymentTypeEnum
    amount: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int
    receipt_id: int
