from sqlalchemy import String, Integer, DateTime, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.database import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.expense import Expense


class Category(Base):
    """
    Expense category with metadata and relationship to expenses.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        server_onupdate=func.now(),
    )

    # One-to-many relationship with Expense
    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="category", cascade="all, delete-orphan", lazy="selectin"
    )

    __table_args__ = (Index("ix_categories_name", "name"),)

    def __repr__(self) -> str:
        return (
            f"<Category(id={self.id}, name='{self.name}', description='{self.description}', "
            f"icon='{self.icon}', color='{self.color}', created_at={self.created_at}, updated_at={self.updated_at})>"
        )
