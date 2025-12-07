from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, datetime, timedelta
from decimal import Decimal
from app.database import get_db
from app.services.expense_service import ExpenseService
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.exceptions import EntityNotFoundException, ValidationException

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


@router.get("/", response_model=List[ExpenseResponse], status_code=status.HTTP_200_OK)
async def get_all_expenses(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve all expenses with pagination.

    Args:
        page: Page number (starts at 1)
        size: Number of items per page (max 100)

    Returns:
        List of expenses with category names
    """
    try:
        skip = (page - 1) * size
        expenses = await ExpenseService.get_all_expenses(db, skip=skip, limit=size)
        return [
            ExpenseResponse(
                id=expense.id,
                amount=Decimal(str(expense.amount)),
                description=expense.description,
                expense_date=expense.expense_date,
                category_id=expense.category_id,
                notes=expense.notes,
                created_at=expense.created_at,
                updated_at=expense.updated_at,
                category_name=(
                    expense.category.name if expense.category else "Uncategorized"
                ),
            )
            for expense in expenses
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve expenses: {str(e)}",
        )


@router.get(
    "/recent", response_model=List[ExpenseResponse], status_code=status.HTTP_200_OK
)
async def get_recent_expenses(
    limit: int = Query(10, ge=1, le=50, description="Number of recent expenses"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve most recent expenses.

    Args:
        limit: Number of expenses to return (max 50)

    Returns:
        List of recent expenses
    """
    try:
        expenses = await ExpenseService.get_all_expenses(db, skip=0, limit=limit)
        return [
            ExpenseResponse(
                id=expense.id,
                amount=Decimal(str(expense.amount)),
                description=expense.description,
                expense_date=expense.expense_date,
                category_id=expense.category_id,
                notes=expense.notes,
                created_at=expense.created_at,
                updated_at=expense.updated_at,
                category_name=(
                    expense.category.name if expense.category else "Uncategorized"
                ),
            )
            for expense in expenses
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve recent expenses: {str(e)}",
        )


@router.get("/summary", status_code=status.HTTP_200_OK)
async def get_expense_summary(db: AsyncSession = Depends(get_db)):
    """
    Get expense totals and statistics.

    Returns:
        Dictionary with total expenses and amount
    """
    try:
        stats = await ExpenseService.get_expense_statistics(db)
        total_amount = await ExpenseService.get_total_expense_amount(db)
        return {**stats, "total_amount": float(total_amount)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve summary: {str(e)}",
        )


@router.get("/analytics/category", status_code=status.HTTP_200_OK)
async def get_spending_by_category(db: AsyncSession = Depends(get_db)):
    """
    Get spending breakdown by category.

    Returns:
        List of categories with total spending
    """
    try:
        from sqlalchemy import select, func
        from app.models.expense import Expense
        from app.models.category import Category

        result = await db.execute(
            select(
                Category.name,
                Category.color,
                func.count(Expense.id).label("count"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .outerjoin(Expense, Category.id == Expense.category_id)
            .group_by(Category.id, Category.name, Category.color)
        )

        return [
            {
                "category": row.name,
                "color": row.color,
                "count": row.count,
                "total": float(row.total),
            }
            for row in result.all()
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve category analytics: {str(e)}",
        )


@router.get("/analytics/monthly", status_code=status.HTTP_200_OK)
async def get_monthly_spending_trends(db: AsyncSession = Depends(get_db)):
    """
    Get monthly spending trends for the last 12 months.

    Returns:
        List of months with total spending
    """
    try:
        from sqlalchemy import select, func, extract
        from app.models.expense import Expense

        # Get last 12 months
        end_date = date.today()
        start_date = end_date - timedelta(days=365)

        result = await db.execute(
            select(
                extract("year", Expense.expense_date).label("year"),
                extract("month", Expense.expense_date).label("month"),
                func.coalesce(func.sum(Expense.amount), 0).label("total"),
            )
            .where(Expense.expense_date >= start_date)
            .group_by(
                extract("year", Expense.expense_date),
                extract("month", Expense.expense_date),
            )
            .order_by(
                extract("year", Expense.expense_date),
                extract("month", Expense.expense_date),
            )
        )

        return [
            {"year": int(row.year), "month": int(row.month), "total": float(row.total)}
            for row in result.all()
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve monthly trends: {str(e)}",
        )


@router.get(
    "/search", response_model=List[ExpenseResponse], status_code=status.HTTP_200_OK
)
async def search_expenses(
    keyword: Optional[str] = Query(None, description="Search keyword in description"),
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    db: AsyncSession = Depends(get_db),
):
    """
    Search expenses by keyword and/or date range.

    Args:
        keyword: Optional keyword to search in description
        start_date: Optional start date
        end_date: Optional end date

    Returns:
        List of matching expenses
    """
    try:
        expenses = []

        if keyword:
            expenses = await ExpenseService.search_expenses(db, keyword)
        elif start_date and end_date:
            expenses = await ExpenseService.get_expenses_by_date_range(
                db, start_date, end_date
            )
        elif start_date:
            expenses = await ExpenseService.get_expenses_by_date_range(
                db, start_date, date.today()
            )
        else:
            # If no filters, return recent expenses
            expenses = await ExpenseService.get_all_expenses(db, skip=0, limit=50)

        return [
            ExpenseResponse(
                id=expense.id,
                amount=Decimal(str(expense.amount)),
                description=expense.description,
                expense_date=expense.expense_date,
                category_id=expense.category_id,
                notes=expense.notes,
                created_at=expense.created_at,
                updated_at=expense.updated_at,
                category_name=(
                    expense.category.name if expense.category else "Uncategorized"
                ),
            )
            for expense in expenses
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search expenses: {str(e)}",
        )


@router.get(
    "/category/{category_id}",
    response_model=List[ExpenseResponse],
    status_code=status.HTTP_200_OK,
)
async def get_expenses_by_category(
    category_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Get all expenses for a specific category.

    Args:
        category_id: The ID of the category

    Returns:
        List of expenses in the category
    """
    try:
        expenses = await ExpenseService.get_expenses_by_category(db, category_id)
        return [
            ExpenseResponse(
                id=expense.id,
                amount=Decimal(str(expense.amount)),
                description=expense.description,
                expense_date=expense.expense_date,
                category_id=expense.category_id,
                notes=expense.notes,
                created_at=expense.created_at,
                updated_at=expense.updated_at,
                category_name=(
                    expense.category.name if expense.category else "Uncategorized"
                ),
            )
            for expense in expenses
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve expenses: {str(e)}",
        )


@router.get(
    "/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK
)
async def get_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single expense by ID.

    Args:
        expense_id: The ID of the expense to retrieve

    Returns:
        Expense details with category name

    Raises:
        404: Expense not found
    """
    try:
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        return ExpenseResponse(
            id=expense.id,
            amount=Decimal(str(expense.amount)),
            description=expense.description,
            expense_date=expense.expense_date,
            category_id=expense.category_id,
            notes=expense.notes,
            created_at=expense.created_at,
            updated_at=expense.updated_at,
            category_name=(
                expense.category.name if expense.category else "Uncategorized"
            ),
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve expense: {str(e)}",
        )


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new expense.

    Args:
        expense_data: Expense creation data

    Returns:
        Created expense

    Raises:
        400: Invalid data
        404: Category not found
    """
    try:
        expense = await ExpenseService.create_expense(db, expense_data)
        return ExpenseResponse(
            id=expense.id,
            amount=Decimal(str(expense.amount)),
            description=expense.description,
            expense_date=expense.expense_date,
            category_id=expense.category_id,
            notes=expense.notes,
            created_at=expense.created_at,
            updated_at=expense.updated_at,
            category_name=(
                expense.category.name if expense.category else "Uncategorized"
            ),
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create expense: {str(e)}",
        )


@router.put(
    "/{expense_id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK
)
async def update_expense(
    expense_id: int, expense_data: ExpenseUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing expense.

    Args:
        expense_id: The ID of the expense to update
        expense_data: Updated expense data

    Returns:
        Updated expense

    Raises:
        404: Expense or category not found
        400: Invalid data
    """
    try:
        expense = await ExpenseService.update_expense(db, expense_id, expense_data)
        return ExpenseResponse(
            id=expense.id,
            amount=Decimal(str(expense.amount)),
            description=expense.description,
            expense_date=expense.expense_date,
            category_id=expense.category_id,
            notes=expense.notes,
            created_at=expense.created_at,
            updated_at=expense.updated_at,
            category_name=(
                expense.category.name if expense.category else "Uncategorized"
            ),
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update expense: {str(e)}",
        )


@router.delete("/{expense_id}", status_code=status.HTTP_200_OK)
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an expense.

    Args:
        expense_id: The ID of the expense to delete

    Returns:
        Success message

    Raises:
        404: Expense not found
    """
    try:
        await ExpenseService.delete_expense(db, expense_id)
        return {"message": f"Expense {expense_id} deleted successfully"}
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete expense: {str(e)}",
        )
