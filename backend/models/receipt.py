from datetime import datetime
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey, Integer, DECIMAL
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.models import Base
from backend.models.mixins import IdIntPkMixin

if TYPE_CHECKING:
    from backend.models import User, Payment, ReceiptProduct


class Receipt(Base, IdIntPkMixin):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("Europe/Kyiv"))
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    total: Mapped[float] = mapped_column(DECIMAL, nullable=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="receipts",
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
