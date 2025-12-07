from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.exceptions import EntityNotFoundException, DuplicateEntityException

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all categories with their expense counts.

    Returns:
        List of categories with expense counts
    """
    try:
        categories_with_counts = (
            await CategoryService.get_categories_with_expense_count(db)
        )
        return [
            CategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                icon=category.icon,
                color=category.color,
                created_at=category.created_at,
                updated_at=category.updated_at,
                expense_count=count,
            )
            for category, count in categories_with_counts
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve categories: {str(e)}",
        )


@router.get("/stats", status_code=status.HTTP_200_OK)
async def get_category_statistics(db: AsyncSession = Depends(get_db)):
    """
    Get category usage statistics.

    Returns:
        Dictionary with category statistics
    """
    try:
        stats = await CategoryService.get_category_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve statistics: {str(e)}",
        )


@router.get("/search", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def search_category_by_name(
    name: str = Query(..., min_length=1, description="Category name to search"),
    db: AsyncSession = Depends(get_db),
):
    """
    Search for a category by name.

    Args:
        name: Category name to search for

    Returns:
        Category if found

    Raises:
        404: Category not found
    """
    try:
        category = await CategoryService.get_category_by_name(db, name)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with name '{name}' not found",
            )
        # Get expense count for this category
        categories_with_counts = (
            await CategoryService.get_categories_with_expense_count(db)
        )
        expense_count = next(
            (count for cat, count in categories_with_counts if cat.id == category.id), 0
        )

        return CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            icon=category.icon,
            color=category.color,
            created_at=category.created_at,
            updated_at=category.updated_at,
            expense_count=expense_count,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search category: {str(e)}",
        )


@router.get(
    "/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single category by ID.

    Args:
        category_id: The ID of the category to retrieve

    Returns:
        Category details with expense count

    Raises:
        404: Category not found
    """
    try:
        category = await CategoryService.get_category_by_id(db, category_id)
        # Get expense count for this category
        categories_with_counts = (
            await CategoryService.get_categories_with_expense_count(db)
        )
        expense_count = next(
            (count for cat, count in categories_with_counts if cat.id == category.id), 0
        )

        return CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            icon=category.icon,
            color=category.color,
            created_at=category.created_at,
            updated_at=category.updated_at,
            expense_count=expense_count,
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve category: {str(e)}",
        )


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new category.

    Args:
        category_data: Category creation data

    Returns:
        Created category

    Raises:
        400: Invalid data
        409: Duplicate category name
    """
    try:
        category = await CategoryService.create_category(db, category_data)
        return CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            icon=category.icon,
            color=category.color,
            created_at=category.created_at,
            updated_at=category.updated_at,
            expense_count=0,
        )
    except DuplicateEntityException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create category: {str(e)}",
        )


@router.put(
    "/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
async def update_category(
    category_id: int, category_data: CategoryUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing category.

    Args:
        category_id: The ID of the category to update
        category_data: Updated category data

    Returns:
        Updated category

    Raises:
        404: Category not found
        409: Duplicate category name
    """
    try:
        category = await CategoryService.update_category(db, category_id, category_data)
        # Get expense count for this category
        categories_with_counts = (
            await CategoryService.get_categories_with_expense_count(db)
        )
        expense_count = next(
            (count for cat, count in categories_with_counts if cat.id == category.id), 0
        )

        return CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            icon=category.icon,
            color=category.color,
            created_at=category.created_at,
            updated_at=category.updated_at,
            expense_count=expense_count,
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except DuplicateEntityException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update category: {str(e)}",
        )


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a category.

    Note: This will cascade delete all expenses in this category.

    Args:
        category_id: The ID of the category to delete

    Returns:
        Success message

    Raises:
        404: Category not found
    """
    try:
        await CategoryService.delete_category(db, category_id)
        return {"message": f"Category {category_id} deleted successfully"}
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete category: {str(e)}",
        )
