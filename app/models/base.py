from datetime import datetime
from typing import List, Optional, Self

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
    def get(cls, id: int, options=None) -> Self | None:
        """Get a model instance by ID."""
        return get_db().session.get(cls, id, options=options)

    @classmethod
    def get_all(cls, options=None) -> List[Self] | None:
        """Get all instances of a model."""
        return get_db().session.query(cls).all()

    def save(self):
        """Save the model instance."""
        get_db().session.add(self)
        get_db().session.commit()
        get_db().session.refresh(self)
        return self

    def delete(self):
        """Save the model instance."""
        get_db().session.delete(self)
        get_db().session.commit()
