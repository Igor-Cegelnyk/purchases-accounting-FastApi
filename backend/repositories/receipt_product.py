from typing import TYPE_CHECKING

from backend.models import ReceiptProduct, Product
from backend.repositories import SqlAlchemyRepository


if TYPE_CHECKING:
    from backend.models import Product, Receipt
    from backend.schemas.receipt import ProductInput


class ReceiptProductRepository(SqlAlchemyRepository):
    model = ReceiptProduct

    async def create_receipt_products(
        self,
        products: list["Product"],
        receipt: "Receipt",
        products_in: list["ProductInput"],
    ) -> list[ReceiptProduct]:
        receipt_products = [
            ReceiptProduct(
                receipt_id=receipt.id,
                product_id=[
                    product.id for product in products if line.name == product.name
                ][0],
                price=line.price,
                quantity=line.quantity,
                total=line.price * line.quantity,
            )
            for line in products_in
        ]
        self.session.add_all(receipt_products)
        await self.session.commit()

        return receipt_products
