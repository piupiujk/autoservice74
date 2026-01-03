"""Модуль для работы с заказами в базе данных."""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import OrderModel
from app.enums import OrderStatusEnum
from app.database_config import async_session_maker


class OrderDAO:
    """Класс для выполнения операций с заказами в базе данных."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_order(
        self,
        user_id: int,
        product_id: int,
        status: OrderStatusEnum = OrderStatusEnum.CREATED
    ) -> OrderModel:
        """Создание нового заказа."""
        order = OrderModel(
            user_id=user_id,
            product_id=product_id,
            status=status
        )
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order
    
    async def get_order(self, order_id: UUID) -> Optional[OrderModel]:
        """Получение заказа по ID."""
        result = await self.db.execute(
            select(OrderModel).where(OrderModel.order_id == order_id)
        )
        return result.scalar_one_or_none()
    
    async def get_orders(self) -> List[OrderModel]:
        """Получение всех заказов."""
        result = await self.db.execute(select(OrderModel))
        return result.scalars().all()
    
    async def update_order(
        self,
        order_id: UUID,
        user_id: int = None,
        product_id: int = None,
        status: OrderStatusEnum = None
    ) -> Optional[OrderModel]:
        """Обновление заказа."""
        order = await self.get_order(order_id)
        if not order:
            return None
        
        if user_id is not None:
            order.user_id = user_id
        if product_id is not None:
            order.product_id = product_id
        if status is not None:
            order.status = status
        
        await self.db.commit()
        await self.db.refresh(order)
        return order
    
    async def delete_order(self, order_id: UUID) -> bool:
        """Удаление заказа. Возвращает True, если заказ был удален."""
        result = await self.db.execute(
            delete(OrderModel).where(OrderModel.order_id == order_id)
        )
        await self.db.commit()
        return result.rowcount > 0
