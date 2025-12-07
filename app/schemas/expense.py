from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class ExpenseBase(BaseModel):
    amount: Decimal = Field(
        ..., gt=0, decimal_places=2, description="Expense amount (must be positive)"
    )
    description: str = Field(..., min_length=1, max_length=255)
    expense_date: date = Field(..., description="Date of expense")
    category_id: int = Field(..., gt=0, description="Category ID")
    notes: Optional[str] = Field(None, max_length=500)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    expense_date: Optional[date] = None
    category_id: Optional[int] = Field(None, gt=0)
    notes: Optional[str] = Field(None, max_length=500)


class ExpenseResponse(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
    category_name: str = Field(..., description="Name of the category")
