from dotenv import load_dotenv

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, \
    async_sessionmaker

from app.config.database import DatabaseSettings

load_dotenv()

settings = DatabaseSettings()

DATABASE_URL = settings.db_url
DATABASE_PARAMS = {'poolclass': NullPool}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession,
                                         expire_on_commit=False)
