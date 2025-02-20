from typing import Generator  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session  

from core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
    ):
        self.engine = create_engine(url, echo=True)  
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def dispose(self) -> None:
        self.engine.dispose()

    def session_getter(self) -> Generator[Session, None, None]:
        with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url)
)

def get_db() -> Generator[Session, None, None]:
    for session in db_helper.session_getter():
        yield session
