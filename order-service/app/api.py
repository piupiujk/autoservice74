from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Body
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database_config import async_session_maker
from app.database.dao import OrderDAO
from app.enums import OrderStatusEnum

router = APIRouter()

async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД."""
    async with async_session_maker() as session:
        yield session

async def get_order_dao(db: AsyncSession = Depends(get_db)) -> OrderDAO:
    """Зависимость для получения экземпляра OrderDAO."""
    return OrderDAO(db)

@router.get('/ping', tags=['healthcheck'])
async def ping() -> dict[str, str]:
    """Проверка работоспособности сервиса."""
    return {'status': 'ok'}

@router.post('/orders', tags=['orders'], status_code=status.HTTP_201_CREATED)
async def create_order(
    user_id: int = Body(...),
    product_id: int = Body(...),
    status: OrderStatusEnum = Body(OrderStatusEnum.CREATED),
    booking_time: datetime = Body(None),
    dao: OrderDAO = Depends(get_order_dao)
) -> dict:
    """Создание нового заказа."""
    order = await dao.create_order(user_id, product_id, status, booking_time)
    
    return {
        'order_id': str(order.order_id),
        'user_id': order.user_id,
        'product_id': order.product_id,
        'status': order.status,
        'booking_time': order.booking_time,
        'created_to': order.created_to,
        'update_to': order.update_to
    }

@router.get('/orders', tags=['orders'])
async def get_orders(dao: OrderDAO = Depends(get_order_dao)) -> list[dict]:
    """Получение списка всех заказов."""
    orders = await dao.get_orders()
    
    return [
        {
            'order_id': str(order.order_id),
            'user_id': order.user_id,
            'product_id': order.product_id,
            'status': order.status,
            'booking_time': order.booking_time,
            'created_to': order.created_to,
            'update_to': order.update_to
        } for order in orders
    ]

@router.get('/orders/{order_id}', tags=['orders'])
async def get_order(
    order_id: UUID,
    dao: OrderDAO = Depends(get_order_dao)
) -> dict:
    """Получение информации о конкретном заказе."""
    order = await dao.get_order(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found'
        )
    
    return {
        'order_id': str(order.order_id),
        'user_id': order.user_id,
        'product_id': order.product_id,
        'status': order.status,
        'booking_time': order.booking_time,
        'created_to': order.created_to,
        'update_to': order.update_to
    }

@router.patch('/orders/{order_id}', tags=['orders'])
async def update_order(
    order_id: UUID,
    user_id: int | None = None,
    product_id: int | None = None,
    status: OrderStatusEnum | None = None,
    dao: OrderDAO = Depends(get_order_dao)
) -> dict:
    """Частичное обновление заказа."""
    order = await dao.update_order(order_id, user_id, product_id, status)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found'
        )
    
    return {
        'order_id': str(order.order_id),
        'user_id': order.user_id,
        'product_id': order.product_id,
        'status': order.status,
        'booking_time': order.booking_time,
        'created_to': order.created_to,
        'update_to': order.update_to
    }

@router.delete('/orders/{order_id}', tags=['orders'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: UUID,
    dao: OrderDAO = Depends(get_order_dao)
):
    """Удаление заказа."""
    deleted = await dao.delete_order(order_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found'
        )
    
    return None