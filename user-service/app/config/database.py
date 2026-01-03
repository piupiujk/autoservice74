from pydantic import Field
from pydantic_settings import BaseSettings

ASYNC_DRIVER = 'postgresql+asyncpg'

class DatabaseSettings(BaseSettings):
    """Настройки приложения.

    Загружает конфигурацию из переменных окружения.
    Предоставляет метод для работы с настройками БД.
    """

    internal_port: int = Field(alias='user_db_internal_port')
    external_port: int = Field(alias='user_db_external_port')

    user: str = Field(alias='user_postgres_user')
    password: str = Field(alias='user_postgres_password')
    host: str = Field(alias='user_postgres_host')
    db_name: str = Field(alias='user_postgres_db')

    @property
    def db_url(self) -> str:
        """URL для асинхронного подключения к PostgreSQL.

        Returns:
            str: Строка подключения.
        """
        return (
            f'{ASYNC_DRIVER}://{self.user}:'
            f'{self.password}@{self.host}:'
            f'{self.internal_port}/{self.db_name}'
        )