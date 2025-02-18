from sqlalchemy import String, Boolean, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base
from backend.models.mixins import IdIntPkMixin


class User(Base, IdIntPkMixin):
    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
