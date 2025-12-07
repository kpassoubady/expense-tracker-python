import pytest
from datetime import datetime, timezone
from app.schemas.response import ApiResponse, PaginatedResponse, ErrorResponse
from app.schemas.category import CategoryResponse


@pytest.fixture
def sample_category() -> CategoryResponse:
    """Create a sample category response for testing."""
    return CategoryResponse(
        id=1,
        name="Food",
        description="Groceries and restaurants",
        icon="fas fa-utensils",
        color="#FF6B6B",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        expense_count=5,
    )


class TestApiResponse:
    """Tests for ApiResponse schema."""

    def test_api_response_with_data(self, sample_category):
        response = ApiResponse[CategoryResponse](
            data=sample_category,
            message="Category retrieved successfully"
        )
        assert response.success is True
        assert response.data is not None
        assert response.data.id == 1
        assert response.data.name == "Food"
        assert response.message == "Category retrieved successfully"

    def test_api_response_default_values(self):
        response = ApiResponse[dict](data={"key": "value"})
        assert response.success is True
        assert response.message == "Success"

    def test_api_response_without_data(self):
        response = ApiResponse[None](success=True, message="Operation completed")
        assert response.data is None

    def test_api_response_serialization(self, sample_category):
        response = ApiResponse[CategoryResponse](data=sample_category)
        json_data = response.model_dump()
        assert "success" in json_data
        assert "data" in json_data
        assert "message" in json_data


class TestPaginatedResponse:
    """Tests for PaginatedResponse schema."""

    def test_paginated_response_create(self, sample_category):
        items = [sample_category]
        response = PaginatedResponse.create(
            items=items,
            total=100,
            page=1,
            size=10
        )
        assert response.items == items
        assert response.total == 100
        assert response.page == 1
        assert response.size == 10
        assert response.pages == 10

    def test_paginated_response_pages_calculation(self):
        # Test with non-even division
        response = PaginatedResponse.create(items=[], total=25, page=1, size=10)
        assert response.pages == 3  # 25 items / 10 per page = 3 pages

    def test_paginated_response_empty(self):
        response = PaginatedResponse.create(items=[], total=0, page=1, size=10)
        assert response.items == []
        assert response.total == 0
        assert response.pages == 0

    def test_paginated_response_serialization(self, sample_category):
        response = PaginatedResponse.create(
            items=[sample_category],
            total=1,
            page=1,
            size=10
        )
        json_data = response.model_dump()
        assert "items" in json_data
        assert "total" in json_data
        assert "page" in json_data
        assert "size" in json_data
        assert "pages" in json_data


class TestErrorResponse:
    """Tests for ErrorResponse schema."""

    def test_error_response_basic(self):
        response = ErrorResponse(
            error="NOT_FOUND",
            message="Resource not found"
        )
        assert response.success is False
        assert response.error == "NOT_FOUND"
        assert response.message == "Resource not found"
        assert response.detail is None

    def test_error_response_with_detail(self):
        response = ErrorResponse(
            error="VALIDATION_ERROR",
            message="Invalid input",
            detail={"field": "amount", "issue": "Must be positive"}
        )
        assert response.success is False
        assert response.detail == {"field": "amount", "issue": "Must be positive"}

    def test_error_response_with_list_detail(self):
        response = ErrorResponse(
            error="VALIDATION_ERROR",
            message="Multiple validation errors",
            detail=[
                {"field": "amount", "message": "Required"},
                {"field": "category_id", "message": "Invalid ID"},
            ]
        )
        assert len(response.detail) == 2

    def test_error_response_serialization(self):
        response = ErrorResponse(error="SERVER_ERROR", message="Internal error")
        json_data = response.model_dump()
        assert json_data["success"] is False
        assert "error" in json_data
        assert "message" in json_data
        assert "detail" in json_data
