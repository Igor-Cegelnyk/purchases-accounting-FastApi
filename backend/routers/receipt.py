import os
from datetime import datetime
from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.params import Depends
from starlette.templating import Jinja2Templates

from backend.config import settings
from backend.config.exceptions import ReceiptException
from backend.database import db_helper
from backend.models import Receipt, Payment, PaymentTypeEnum
from backend.repositories.payment import PaymentRepository
from backend.repositories.product import ProductRepository
from backend.repositories.receipt import ReceiptRepository
from backend.repositories.receipt_product import ReceiptProductRepository
from backend.routers.dependencies import validate_auth_user, get_receipt_repository
from backend.schemas.receipt import ReceiptCreate, ReceiptRead
from backend.schemas.user import UserRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


templates = Jinja2Templates(directory=os.getenv("TEMPLATE_DIR", "templates"))

router = APIRouter(
    prefix=settings.api_prefix.receipt,
    tags=["Receipt"],
)


@router.post(
    "/create_receipt",
    summary="Створення нового чека",
)
async def create_receipt(
    receipt_in: ReceiptCreate,
    user: UserRead = Depends(validate_auth_user),
    session: "AsyncSession" = Depends(db_helper.session_getter),
) -> ReceiptRead:
    receipt_repo = ReceiptRepository(session=session)
    products = await ProductRepository(session=session).bulk_create_products(
        [product.name for product in receipt_in.products]
    )
    receipt_cost = sum(
        [product.quantity * product.price for product in receipt_in.products]
    )
    receipt = await receipt_repo.create(Receipt(user_id=user.id, total=receipt_cost))
    await PaymentRepository(session=session).create(
        Payment(**receipt_in.payment.model_dump(), receipt_id=receipt.id)
    )
    await ReceiptProductRepository(session=session).create_receipt_products(
        products=products, receipt=receipt, products_in=receipt_in.products
    )
    result = await receipt_repo.get_receipts(receipt_id=receipt.id)

    return ReceiptRead(**result[0])


@router.get(
    "/get_receipts",
    summary="Перегляд власних чеків",
)
async def get_receipts(
    receipt_id: int | None = None,
    receipt_cost: float | None = None,
    payment_type: PaymentTypeEnum | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = 10,
    offset: int = 0,
    user: UserRead = Depends(validate_auth_user),
    receipt_repo: ReceiptRepository = Depends(get_receipt_repository),
) -> list[ReceiptRead]:
    receipts = await receipt_repo.get_receipts(
        user_id=user.id,
        receipt_id=receipt_id,
        receipt_cost=receipt_cost,
        payment_type=payment_type,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )

    return [ReceiptRead(**receipt) for receipt in receipts]


@router.get(
    "/check_receipt",
    summary="Перегляд чеку за унікальним номером",
    response_class=HTMLResponse,
)
async def check_receipt(
    request: Request,
    receipt_id: int,
    line_length: int = Query(default=35, ge=15, le=100),
    receipt_repo: ReceiptRepository = Depends(get_receipt_repository),
):
    receipt = await receipt_repo.get_by_id(receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=404,
            detail=ReceiptException.not_found,
        )

    return templates.TemplateResponse(
        "receipt.html",
        {
            "request": request,
            "receipt": receipt,
            "line_length": line_length * 10,
            "create_at_formatted": receipt.created_at.strftime("%d.%m.%Y %H:%M"),
        },
    )
