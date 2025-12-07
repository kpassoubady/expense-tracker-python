from sqlalchemy import Integer, String, Date, DateTime, Numeric, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date, timezone
from app.database import Base
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.category import Category


class Expense(Base):
    """
    Represents a single expense record.
    """
        
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    expense_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        server_onupdate=func.now(),
    )

    # Many-to-one relationship with Category
    category: Mapped["Category"] = relationship(
        back_populates="expenses", lazy="selectin"
    )

    __table_args__ = (Index("ix_expenses_category_id", "category_id"),Index("ix_expenses_expense_date", "expense_date"))

    def __repr__(self) -> str:
        return (
            f"<Expense(id={self.id}, amount={self.amount}, description='{self.description}', "
            f"expense_date={self.expense_date}, category_id={self.category_id}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )
