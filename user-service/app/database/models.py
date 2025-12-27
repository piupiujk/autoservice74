"""Модуль моделей SQLAlchemy для пользователей."""
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship




class BaseModel(AsyncAttrs, DeclarativeBase):
    pass

class UserModel(BaseModel):
    """Модель пользователей.

    Args:
        id_: id пользователя
        first_name: Имя пользователя
        last_name: Фамилия пользователя
        patronymic: Отчество пользователя
        email: Контактный email
        phone: Контактный номер телефона
        bonus_score: Бонусные баллы
        created_to: Дата и время создания пользователя
        update_to: Дата и время обновления пользователя
    """

    __tablename__ = 'users'

    id_: Mapped[int] = mapped_column(
        name='id',
        type_=Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        name='first_name',
        type_=String(length=100),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        name='last_name',
        type_=String(length=100),
        nullable=False,
    )
    patronymic: Mapped[str | None] = mapped_column(
        name='patronymic',
        type_=String(length=100),
        nullable=True,
    )
    email: Mapped[str] = mapped_column(
        name='email',
        type_=String(length=150),
        nullable=False,
        unique=True,
        index=True,
    )
    phone: Mapped[str] = mapped_column(
        name='phone',
        type_=String(length=20),
        nullable=False,
        unique=True,
        index=True,
    )
    bonus_score: Mapped[int] = mapped_column(
        name='bonus_score',
        type_=Integer,
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
