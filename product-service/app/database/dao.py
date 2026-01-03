"""Модуль для работы с продуктами в базе данных."""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import ProductModel


class ProductDAO:
    """Класс для выполнения операций с продуктами в базе данных."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_product(
        self,
        name: str,
        schedule_time: int,
        price: int,
        is_active: bool = True
    ) -> ProductModel:
        """Создание нового продукта."""
        product = ProductModel(
            name=name,
            schedule_time=schedule_time,
            price=price,
            is_active=is_active
        )
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def get_product(self, product_id: int) -> Optional[ProductModel]:
        """Получение продукта по ID."""
        result = await self.db.execute(
            select(ProductModel).where(ProductModel.id_ == product_id)
        )
        return result.scalar_one_or_none()
    
    async def get_products(self) -> List[ProductModel]:
        """Получение всех продуктов."""
        result = await self.db.execute(select(ProductModel))
        return result.scalars().all()
    
    async def update_product(
        self,
        product_id: int,
        name: str = None,
        description: str = None,
        price: float = None,
        category: str = None,
        in_stock: bool = None
    ) -> Optional[ProductModel]:
        """Обновление продукта."""
        product = await self.get_product(product_id)
        if not product:
            return None
        
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if category is not None:
            product.category = category
        if in_stock is not None:
            product.in_stock = in_stock
        
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def delete_product(self, product_id: int) -> bool:
        """Удаление продукта. Возвращает True, если продукт был удален."""
        result = await self.db.execute(
            delete(ProductModel).where(ProductModel.id_ == product_id)
        )
        await self.db.commit()
        return result.rowcount > 0