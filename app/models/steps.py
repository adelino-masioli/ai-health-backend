"""Steps SQLAlchemy model."""

from datetime import date as date_type

from sqlalchemy import Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Steps(Base):
    """Daily steps count stored in the database."""

    __tablename__ = "steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
