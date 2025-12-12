from fastapi import APIRouter

router = APIRouter()

@router.get('/ping', tags=['healthcheck'])
async def ping() -> dict[str, str]:
    """Проверка работоспособности сервиса.

    Этот эндпоинт предоставляет базовую проверку состояния сервиса.
    Используется для мониторинга доступности API.

    Returns:
        dict: Словарь с информацией о статусе сервиса в формате:
            {'status': 'ok'}
    """
    return {'status': 'ok'}