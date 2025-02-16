from sqlalchemy.ext.asyncio import create_async_engine ,async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.config import settings

class DatabaseHelper:

    def __init__(self,url : str,echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind= self.engine,
            autoflush=False,
            autocommit = False,
            expire_on_commit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_factory() as session:
            yield session

db_helper = DatabaseHelper(url = settings.db_url, echo=settings.db_echo)