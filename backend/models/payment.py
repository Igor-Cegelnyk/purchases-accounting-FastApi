import enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models import Base
from backend.models.mixins import IdIntPkMixin


if TYPE_CHECKING:
    from backend.models import Receipt


class PaymentTypeEnum(str, enum.Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class Payment(Base, IdIntPkMixin):
    receipt_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    type: Mapped[PaymentTypeEnum] = mapped_column(
        Enum(PaymentTypeEnum),
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(DECIMAL, nullable=False)

    receipt: Mapped["Receipt"] = relationship(
        "Receipt",
        back_populates="payment",
    )
