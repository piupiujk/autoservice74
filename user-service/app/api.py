from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database_config import async_session_maker
from app.database.dao import UserDAO

router = APIRouter()

async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД."""
    async with async_session_maker() as session:
        yield session

async def get_user_dao(db: AsyncSession = Depends(get_db)) -> UserDAO:
    """Зависимость для получения экземпляра UserDAO."""
    return UserDAO(db)

@router.get('/ping', tags=['healthcheck'])
async def ping() -> dict[str, str]:
    """Проверка работоспособности сервиса."""
    return {'status': 'ok'}

@router.post('/users', tags=['users'], status_code=status.HTTP_201_CREATED)
async def create_user(
    first_name: str,
    last_name: str,
    patronymic: str | None = None,
    email: str = None,
    phone: str = None,
    bonus_score: int = 0,
    dao: UserDAO = Depends(get_user_dao)
) -> dict:
    """Создание нового пользователя."""
    user = await dao.create_user(first_name, last_name, patronymic, email, phone, bonus_score)
    
    return {
        'id_': user.id_,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'patronymic': user.patronymic,
        'email': user.email,
        'phone': user.phone,
        'bonus_score': user.bonus_score,
        'created_to': user.created_to,
        'update_to': user.update_to
    }

@router.get('/users', tags=['users'])
async def get_users(dao: UserDAO = Depends(get_user_dao)) -> list[dict]:
    """Получение списка всех пользователей."""
    users = await dao.get_users()
    
    return [
        {
            'id_': user.id_,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'patronymic': user.patronymic,
            'email': user.email,
            'phone': user.phone,
            'bonus_score': user.bonus_score,
            'created_to': user.created_to,
            'update_to': user.update_to
        } for user in users
    ]

@router.get('/users/{user_id}', tags=['users'])
async def get_user(
    user_id: int,
    dao: UserDAO = Depends(get_user_dao)
) -> dict:
    """Получение информации о конкретном пользователе."""
    user = await dao.get_user(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    return {
        'id_': user.id_,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'patronymic': user.patronymic,
        'email': user.email,
        'phone': user.phone,
        'bonus_score': user.bonus_score,
        'created_to': user.created_to,
        'update_to': user.update_to
    }

@router.patch('/users/{user_id}', tags=['users'])
async def update_user(
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    patronymic: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    bonus_score: int | None = None,
    car_info: str | None = None,
    additional_info: str | None = None,
    dao: UserDAO = Depends(get_user_dao)
) -> dict:
    """Частичное обновление пользователя."""
    user = await dao.update_user(user_id, first_name, last_name, patronymic, email, phone, bonus_score, car_info, additional_info)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    return {
        'id_': user.id_,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'patronymic': user.patronymic,
        'email': user.email,
        'phone': user.phone,
        'bonus_score': user.bonus_score,
        'car_info': user.car_info,
        'additional_info': user.additional_info,
        'created_to': user.created_to,
        'update_to': user.update_to
    }

@router.delete('/users/{user_id}', tags=['users'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    dao: UserDAO = Depends(get_user_dao)
):
    """Удаление пользователя."""
    deleted = await dao.delete_user(user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    return None