from datetime import datetime
from typing import Optional, Self

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.db import get_db


class Base(DeclarativeBase):
    """The common SQLAlchemy ORM base that all standard ORM Mapped Classes should inherit from."""

    # Common fields that all models should contain.
    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow)
    updated: Mapped[Optional[datetime]] = mapped_column(
        insert_default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted: Mapped[datetime]

    @classmethod
    async def get(cls, id: int, db: AsyncSession) -> Self | None:
        """Get a model instance by ID."""
        result = await db.execute(select(cls).filter(cls.id == id))
        return result.scalars().first()

    @classmethod
    async def get_all(cls, db: AsyncSession):
        """Get all instances of a model."""
        result = await db.execute(select(cls))
        return result.scalars().all()

    async def save(self, db: AsyncSession):
        async with db.begin():
            db.add(self)
        await db.commit()
        await db.refresh(self)
