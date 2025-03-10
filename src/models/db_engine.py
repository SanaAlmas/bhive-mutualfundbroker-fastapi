from config import config_obj
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

async_engine = create_async_engine(config_obj.DATABASE_URL, echo=True, future=True)

session_maker = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session

async def commit_session(session: AsyncSession):
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
