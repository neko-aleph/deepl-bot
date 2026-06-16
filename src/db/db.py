from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from decouple import config

from .model import Base

DB_PATH = config("SQLITE_PATH")

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True)

session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_db():
    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
