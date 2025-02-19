from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.models import Base
from backend.models.mixins import IdIntPkMixin

if TYPE_CHECKING:
    from backend.models import User, Payment, ReceiptProduct


class Receipt(Base, IdIntPkMixin):
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="receipts",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    payment: Mapped["Payment"] = relationship(
        "Payment",
        back_populates="receipt",
        uselist=False,
        lazy="joined",
    )

    products: Mapped[list["ReceiptProduct"]] = relationship(
        "ReceiptProduct",
        back_populates="receipt",
        lazy="selectin",
    )
