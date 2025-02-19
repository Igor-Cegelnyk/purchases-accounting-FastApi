from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi.params import Depends

from backend.config import settings
from backend.database import db_helper
from backend.models import Receipt, Payment
from backend.repositories.payment import PaymentRepository
from backend.repositories.product import ProductRepository
from backend.repositories.receipt import ReceiptRepository
from backend.repositories.receipt_product import ReceiptProductRepository
from backend.routers.dependencies import validate_auth_user
from backend.schemas.receipt import ReceiptCreate, ReceiptRead
from backend.schemas.user import UserRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix=settings.api_prefix.receipt,
    tags=["Receipt"],
)


@router.post("/create_receipt")
async def create_receipt(
    receipt_in: ReceiptCreate,
    user: UserRead = Depends(validate_auth_user),
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> ReceiptRead:
    receipt_repo = ReceiptRepository(session=session)
    products = await ProductRepository(session=session).bulk_create_products(
        [product.name for product in receipt_in.products]
    )
    receipt = await receipt_repo.create(Receipt(user_id=user.id))
    await PaymentRepository(session=session).create(
        Payment(**receipt_in.payment.model_dump(), receipt_id=receipt.id)
    )
    await ReceiptProductRepository(session=session).create_receipt_products(
        products=products, receipt=receipt, products_in=receipt_in.products
    )
    result = await receipt_repo.get_by_id(id=receipt.id)

    return ReceiptRead(**result)
