from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models import Base
from backend.models.mixins import IdIntPkMixin


class Product(Base, IdIntPkMixin):
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
