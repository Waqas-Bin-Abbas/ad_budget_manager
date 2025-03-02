from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Campaign(Base):
    """
    Represents a marketing campaign associated with a brand.

    Relationships:
        brand: The brand associated with the campaign.
    """

    __tablename__ = "campaigns"

    name: Mapped[str] = mapped_column(nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    dayparting_start: Mapped[int] = mapped_column(nullable=True)
    dayparting_end: Mapped[int] = mapped_column(nullable=True)

    brand = relationship("Brand", back_populates="campaigns")
