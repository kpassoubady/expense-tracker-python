from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Generic API response wrapper with success status, data, and message."""
    
    success: bool = Field(default=True, description="Indicates if the request was successful")
    data: Optional[T] = Field(default=None, description="Response payload")
    message: str = Field(default="Success", description="Human-readable response message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "data": {"id": 1, "name": "Example"},
                    "message": "Resource retrieved successfully"
                }
            ]
        }
    }


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response for list endpoints."""
    
    items: List[T] = Field(default_factory=list, description="List of items for the current page")
    total: int = Field(description="Total number of items across all pages")
    page: int = Field(ge=1, description="Current page number (1-indexed)")
    size: int = Field(ge=1, le=100, description="Number of items per page")
    pages: int = Field(description="Total number of pages")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}],
                    "total": 50,
                    "page": 1,
                    "size": 10,
                    "pages": 5
                }
            ]
        }
    }

    @classmethod
    def create(cls, items: List[T], total: int, page: int, size: int) -> "PaginatedResponse[T]":
        """Factory method to create a paginated response with calculated pages."""
        pages = (total + size - 1) // size if size > 0 else 0
        return cls(items=items, total=total, page=page, size=size, pages=pages)


class ErrorResponse(BaseModel):
    """Standard error response for API errors."""
    
    success: bool = Field(default=False, description="Always False for error responses")
    error: str = Field(description="Error code or type")
    message: str = Field(description="Human-readable error message")
    detail: Optional[Any] = Field(default=None, description="Additional error details")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": False,
                    "error": "NOT_FOUND",
                    "message": "Resource not found",
                    "detail": {"resource": "expense", "id": 999}
                },
                {
                    "success": False,
                    "error": "VALIDATION_ERROR",
                    "message": "Invalid input data",
                    "detail": [{"field": "amount", "message": "Must be positive"}]
                }
            ]
        }
    }
