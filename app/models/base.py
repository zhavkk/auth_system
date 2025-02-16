from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
from sqlalchemy import MetaData
class Base(DeclarativeBase):
    __abstract__ = True

    metadata =MetaData(
        naming_convention=settings.naming_convention,
    )
    id: Mapped[int] = mapped_column(primary_key=True)

