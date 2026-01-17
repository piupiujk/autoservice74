"""Модуль для работы с пользователями в базе данных."""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserModel


class UserDAO:
    """Класс для выполнения операций с пользователями в базе данных."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(
        self,
        first_name: str,
        last_name: str,
        patronymic: str | None = None,
        email: str = None,
        phone: str = None,
        bonus_score: int = 0
    ) -> UserModel:
        """Создание нового пользователя."""
        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            email=email,
            phone=phone,
            bonus_score=bonus_score
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_user(self, user_id: int) -> Optional[UserModel]:
        """Получение пользователя по ID."""
        result = await self.db.execute(
            select(UserModel).where(UserModel.id_ == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_users(self) -> List[UserModel]:
        """Получение всех пользователей."""
        result = await self.db.execute(select(UserModel))
        return result.scalars().all()
    
    async def update_user(
        self,
        user_id: int,
        first_name: str = None,
        last_name: str = None,
        patronymic: str = None,
        email: str = None,
        phone: str = None,
        bonus_score: int = None,
        car_info: str = None,
        additional_info: str = None
    ) -> Optional[UserModel]:
        """Обновление пользователя."""
        user = await self.get_user(user_id)
        if not user:
            return None
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if patronymic is not None:
            user.patronymic = patronymic
        if email is not None:
            user.email = email
        if phone is not None:
            user.phone = phone
        if bonus_score is not None:
            user.bonus_score = bonus_score
        if car_info is not None:
            user.car_info = car_info
        if additional_info is not None:
            user.additional_info = additional_info
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя. Возвращает True, если пользователь был удален."""
        result = await self.db.execute(
            delete(UserModel).where(UserModel.id_ == user_id)
        )
        await self.db.commit()
        return result.rowcount > 0