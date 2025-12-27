"""Модуль моделей SQLAlchemy для услуг."""
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(AsyncAttrs, DeclarativeBase):
    pass

class ProductModel(BaseModel):
    """Модель услуг

    Args:
        id_: id услуги
        name: Название услуги
        schedule_time: Примерное время исполнения услуги в минутах
        price: Примерная цена услуги
        created_to: Дата и время создания услуги
        update_to: Дата и время обновления услуги

    """

    __tablename__ = 'products'

    id_: Mapped[int] = mapped_column(
        name='id',
        type_=Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        name='name',
        type_=String(length=100),
        nullable=False,
    )
    schedule_time: Mapped[int] = mapped_column(
        name='schedule_time',
        type_=Integer,
        nullable=False,
    )
    price: Mapped[int] = mapped_column(
        name='price',
        type_=Integer,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        name='is_active',
        type_=Boolean,
        default=True,
        nullable=False,
    )
    created_to: Mapped[datetime] = mapped_column(
        name='created_to',
        type_=DateTime(timezone=True),
        server_default=func.now(),
    )
    update_to: Mapped[datetime] = mapped_column(
        name='update_to',
        type_=DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
