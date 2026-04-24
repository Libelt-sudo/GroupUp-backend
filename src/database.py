from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .config import settings

from .models import Base


engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_db_session():
    async with AsyncSessionLocal() as session:
        yield session