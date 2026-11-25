from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Parent of every model; Alembic reads the tables from `Base.metadata`."""
