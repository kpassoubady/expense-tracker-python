from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    icon: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(
        None,
        min_length=7,
        max_length=7,
        pattern=r"^#[A-Fa-f0-9]{6}$",
        description="Hex color code (e.g. #FF5733)",
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    icon: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(
        None,
        min_length=7,
        max_length=7,
        pattern=r"^#[A-Fa-f0-9]{6}$",
        description="Hex color code (e.g. #FF5733)",
    )


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
    expense_count: int = Field(
        ..., ge=0, description="Number of expenses in this category"
    )
