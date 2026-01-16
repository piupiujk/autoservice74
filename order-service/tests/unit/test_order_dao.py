import pytest
from uuid import uuid4

from app.enums import OrderStatusEnum
from app.database.dao import OrderDAO


@pytest.mark.asyncio
async def test_create_order_success(db_session):
    # Создаем DAO
    dao = OrderDAO(db_session)
    
    # Создаем заказ
    order = await dao.create_order(
        user_id=1,
        product_id=1,
        status=OrderStatusEnum.CREATED
    )
    
    # Проверяем результат
    assert order.user_id == 1
    assert order.product_id == 1
    assert order.status == OrderStatusEnum.CREATED
    assert order.order_id is not None

@pytest.mark.asyncio
async def test_get_order_success(db_session, clean_db):
    # Создаем заказ
    dao = OrderDAO(db_session)
    created_order = await dao.create_order(1, 1)
    
    # Получаем заказ
    fetched_order = await dao.get_order(created_order.order_id)
    
    # Проверяем
    assert fetched_order is not None
    assert fetched_order.id_ == created_order.id_


@pytest.mark.asyncio
async def test_get_order_not_found(db_session):
    dao = OrderDAO(db_session)
    order = await dao.get_order(uuid4())
    assert order is None

@pytest.mark.asyncio
async def test_update_order_status(db_session, clean_db):
    dao = OrderDAO(db_session)
    order = await dao.create_order(1, 1)
    
    # Обновляем статус
    updated_order = await dao.update_order(
        order.order_id,
        status=OrderStatusEnum.IN_PROGRESS
    )
    
    assert updated_order.status == OrderStatusEnum.IN_PROGRESS

@pytest.mark.asyncio
async def test_delete_order(db_session, clean_db):
    dao = OrderDAO(db_session)
    order = await dao.create_order(1, 1)
    
    # Удаляем заказ
    result = await dao.delete_order(order.order_id)
    assert result is True
    
    # Проверяем, что заказ действительно удален
    deleted_order = await dao.get_order(order.order_id)
    assert deleted_order is None