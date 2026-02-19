from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings


class DatabaseEngine:

    def __init__(self, db_url: str):
        self.engine = create_async_engine(url=db_url)
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session
            await session.close()


db_engine = DatabaseEngine(db_url=settings.database_url)
