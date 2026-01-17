"""Модуль моделей SQLAlchemy для заказов."""
from datetime import datetime
import uuid

from app.enums import OrderStatusEnum

from sqlalchemy import Integer, DateTime, func, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PgEnum


class BaseModel(AsyncAttrs, DeclarativeBase):
    pass


class OrderModel(BaseModel):
    """Модель заказов.


    Args:
        id_: id записи
        order_id: id заказа (UUID)
        user_id: id пользователя
        product_id: id услуги
        status: Статус заказа
        booking_time: Время записи на обслуживание
        created_to: Дата и время создания заказа
        update_to: Дата и время обновления заказа
    """

    __tablename__ = 'orders'

    id_: Mapped[int] = mapped_column(
        name='id',
        type_=Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        name='order_id',
        type_=UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        name='user_id',
        type_=Integer,
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        name='product_id',
        type_=Integer,
        nullable=False,
    )
    status: Mapped[OrderStatusEnum] = mapped_column(
        PgEnum(
            OrderStatusEnum,
            name='order_status',
            create_type=False, # после первой миграции заменить на False
        ),
        name='status',
        nullable=False,
    )
    booking_time: Mapped[datetime] = mapped_column(
        name='booking_time',
        type_=DateTime(timezone=True),
        nullable=True,
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
