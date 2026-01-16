import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database_config import async_session_maker
from app.database.models import BaseModel
from app.main import app

# Тестовая база данных
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
async def db_session():
    # Создаем таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    
    async with test_async_session() as session:
        yield session
    
    # Удаляем таблицы после тестов
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture
async def clean_db(db_session):
    # Очищаем данные после каждого теста
    yield db_session
    await db_session.rollback()

@pytest.fixture
def http_client() -> TestClient:
    """Фикстура для тестового клиента FastAPI.

    Returns:
        TestClient: Клиент для тестирования FastAPI приложений.
    """
    return TestClient(app)
