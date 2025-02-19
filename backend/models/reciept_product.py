from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.models import Base, Receipt
from backend.models.mixins import IdIntPkMixin

if TYPE_CHECKING:
    from backend.models import Receipt, Product


class ReceiptProduct(Base, IdIntPkMixin):
    receipt_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )
    price: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    total: Mapped[float] = mapped_column(DECIMAL, nullable=False)

    receipt: Mapped["Receipt"] = relationship("Receipt", back_populates="products")
    product: Mapped["Product"] = relationship("Product", lazy="joined")
