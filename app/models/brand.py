from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base


class Brand(Base):
    """
    Represents a brand in the system. The Brand model holds information about
    a brand's name, budget limits, and the amount spent.

    Relationships:
        campaigns: The list of Campaigns associated with the brand.
    """

    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    daily_budget: Mapped[float] = mapped_column(nullable=False)
    monthly_budget: Mapped[float] = mapped_column(nullable=False)
    daily_spent: Mapped[float] = mapped_column(default=0.0)
    monthly_spent: Mapped[float] = mapped_column(default=0.0)

    campaigns = relationship("Campaign", back_populates="brand")
