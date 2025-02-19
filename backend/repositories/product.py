from typing import Sequence, Any, List

from sqlalchemy import select, Row, RowMapping

from backend.models import Product
from backend.repositories import SqlAlchemyRepository


class ProductRepository(SqlAlchemyRepository):
    model = Product

    async def get_products_by_names(self, product_names: list[str]) -> List[Product]:
        stmt = select(Product).where(Product.name.in_(product_names))
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def bulk_create_products(self, product_names: list[str]) -> List[Product]:
        existing_products = await self.get_products_by_names(product_names)
        new_products = [
            Product(name=name)
            for name in product_names
            if name not in {product.name for product in existing_products}
        ]

        if new_products:
            self.session.add_all(new_products)
            await self.session.flush()
        existing_products.extend(new_products)

        return existing_products
