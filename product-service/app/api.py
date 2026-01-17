from fastapi import APIRouter, HTTPException, status, Depends, Body
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database_config import async_session_maker
from app.database.dao import ProductDAO

router = APIRouter()

async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД."""
    async with async_session_maker() as session:
        yield session

async def get_product_dao(db: AsyncSession = Depends(get_db)) -> ProductDAO:
    """Зависимость для получения экземпляра ProductDAO."""
    return ProductDAO(db)

@router.get('/ping', tags=['healthcheck'])
async def ping() -> dict[str, str]:
    """Проверка работоспособности сервиса."""
    return {'status': 'ok'}

@router.post('/products', tags=['products'], status_code=status.HTTP_201_CREATED)
async def create_product(
    name: str = Body(...),
    schedule_time: int = Body(...),
    price: int = Body(...),
    is_active: bool = Body(True),
    description: str = Body(None),
    dao: ProductDAO = Depends(get_product_dao)
) -> dict:
    """Создание новой услуги."""
    product = await dao.create_product(name, schedule_time, price, is_active, description)
    
    return {
        'id_': product.id_,
        'name': product.name,
        'description': product.description,
        'schedule_time': product.schedule_time,
        'price': product.price,
        'is_active': product.is_active,
        'created_to': product.created_to,
        'update_to': product.update_to
    }

@router.get('/products', tags=['products'])
async def get_products(dao: ProductDAO = Depends(get_product_dao)) -> list[dict]:
    """Получение списка всех активных услуг."""
    products = await dao.get_products()
    
    return [
        {
            'id_': product.id_,
            'name': product.name,
            'description': getattr(product, 'description', None),
            'schedule_time': product.schedule_time,
            'price': product.price,
            'is_active': product.is_active,
            'created_to': product.created_to,
            'update_to': product.update_to
        } for product in products
    ]

@router.get('/products/{product_id}', tags=['products'])
async def get_product(
    product_id: int,
    dao: ProductDAO = Depends(get_product_dao)
) -> dict:
    """Получение информации о конкретной услуге."""
    product = await dao.get_product(product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    
    return {
        'id_': product.id_,
        'name': product.name,
        'schedule_time': product.schedule_time,
        'price': product.price,
        'is_active': product.is_active,
        'created_to': product.created_to,
        'update_to': product.update_to
    }

@router.patch('/products/{product_id}', tags=['products'])
async def update_product(
    product_id: int,
    name: str | None = None,
    description: str | None = None,
    schedule_time: int | None = None,
    price: int | None = None,
    is_active: bool | None = None,
    dao: ProductDAO = Depends(get_product_dao)
) -> dict:
    """Частичное обновление услуги."""
    product = await dao.update_product(product_id, name, description, schedule_time, price, is_active)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    
    return {
        'id_': product.id_,
        'name': product.name,
        'description': product.description,
        'schedule_time': product.schedule_time,
        'price': product.price,
        'is_active': product.is_active,
        'created_to': product.created_to,
        'update_to': product.update_to
    }

@router.delete('/products/{product_id}', tags=['products'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    dao: ProductDAO = Depends(get_product_dao)
):
    """Удаление услуги."""
    deleted = await dao.delete_product(product_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    
    return None