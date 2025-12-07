from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date
from decimal import Decimal
import os

from app.database import get_db
from app.services.category_service import CategoryService
from app.services.expense_service import ExpenseService
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.exceptions import EntityNotFoundException, DuplicateEntityException, ValidationException

router = APIRouter(tags=["Web Pages"])

# Jinja2 templates setup
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))

# Dashboard Routes
@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Render the main dashboard with key metrics.
    """
    try:
        # Get summary statistics
        expense_stats = await ExpenseService.get_expense_statistics(db)
        total_amount = await ExpenseService.get_total_expense_amount(db)
        category_stats = await CategoryService.get_category_statistics(db)
        recent_expenses = await ExpenseService.get_all_expenses(db, skip=0, limit=5)
        
        return templates.TemplateResponse("home/dashboard.html", {
            "request": request,
            "total_expenses": expense_stats.get("total_expenses", 0),
            "total_amount": float(total_amount),
            "category_count": category_stats.get("total_categories", 0),
            "recent_expenses": recent_expenses
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Failed to load dashboard: {str(e)}"
        })

# Category Routes
@router.get("/categories", response_class=HTMLResponse)
async def list_categories(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Display all categories with expense counts.
    """
    try:
        categories_with_counts = await CategoryService.get_categories_with_expense_count(db)
        return templates.TemplateResponse("categories/list.html", {
            "request": request,
            "categories": categories_with_counts
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Failed to load categories: {str(e)}"
        })

@router.get("/categories/new", response_class=HTMLResponse)
async def new_category_form(request: Request):
    """
    Show form to create a new category.
    """
    return templates.TemplateResponse("categories/form.html", {
        "request": request,
        "is_edit": False
    })

@router.post("/categories", response_class=RedirectResponse)
async def create_category(
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    icon: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle category creation form submission.
    """
    try:
        category_data = CategoryCreate(
            name=name,
            description=description,
            icon=icon,
            color=color
        )
        await CategoryService.create_category(db, category_data)
        return RedirectResponse(url="/categories", status_code=status.HTTP_303_SEE_OTHER)
    except DuplicateEntityException as e:
        return templates.TemplateResponse("categories/form.html", {
            "request": request,
            "is_edit": False,
            "error": e.message,
            "name": name,
            "description": description,
            "icon": icon,
            "color": color
        })
    except Exception as e:
        return templates.TemplateResponse("categories/form.html", {
            "request": request,
            "is_edit": False,
            "error": f"Failed to create category: {str(e)}",
            "name": name,
            "description": description,
            "icon": icon,
            "color": color
        })

@router.get("/categories/{category_id}/edit", response_class=HTMLResponse)
async def edit_category_form(request: Request, category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Show form to edit an existing category.
    """
    try:
        category = await CategoryService.get_category_by_id(db, category_id)
        return templates.TemplateResponse("categories/form.html", {
            "request": request,
            "category": category,
            "is_edit": True
        })
    except EntityNotFoundException as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": e.message
        })

@router.post("/categories/{category_id}/edit", response_class=RedirectResponse)
async def update_category(
    request: Request,
    category_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    icon: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle category update form submission.
    """
    try:
        category_data = CategoryUpdate(
            name=name,
            description=description,
            icon=icon,
            color=color
        )
        await CategoryService.update_category(db, category_id, category_data)
        return RedirectResponse(url="/categories", status_code=status.HTTP_303_SEE_OTHER)
    except (EntityNotFoundException, DuplicateEntityException) as e:
        category = await CategoryService.get_category_by_id(db, category_id)
        return templates.TemplateResponse("categories/form.html", {
            "request": request,
            "category": category,
            "is_edit": True,
            "error": e.message
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Failed to update category: {str(e)}"
        })

@router.post("/categories/{category_id}/delete", response_class=RedirectResponse)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Handle category deletion.
    """
    try:
        await CategoryService.delete_category(db, category_id)
        return RedirectResponse(url="/categories", status_code=status.HTTP_303_SEE_OTHER)
    except EntityNotFoundException:
        return RedirectResponse(url="/categories", status_code=status.HTTP_303_SEE_OTHER)

# Expense Routes
@router.get("/expenses", response_class=HTMLResponse)
async def list_expenses(
    request: Request,
    category_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Display all expenses with optional category filtering.
    """
    try:
        if category_id:
            expenses = await ExpenseService.get_expenses_by_category(db, category_id)
        else:
            expenses = await ExpenseService.get_all_expenses(db, skip=0, limit=100)
        
        categories = await CategoryService.get_all_categories(db)
        
        return templates.TemplateResponse("expenses/list.html", {
            "request": request,
            "expenses": expenses,
            "categories": categories,
            "selected_category": category_id
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Failed to load expenses: {str(e)}"
        })

@router.get("/expenses/new", response_class=HTMLResponse)
async def new_expense_form(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Show form to create a new expense.
    """
    try:
        categories = await CategoryService.get_all_categories(db)
        return templates.TemplateResponse("expenses/form.html", {
            "request": request,
            "categories": categories,
            "today": date.today().isoformat(),
            "is_edit": False
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Failed to load form: {str(e)}"
        })

@router.post("/expenses", response_class=RedirectResponse)
async def create_expense(
    request: Request,
    amount: str = Form(...),
    description: str = Form(...),
    expense_date: str = Form(...),
    category_id: int = Form(...),
    notes: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle expense creation form submission.
    """
    try:
        expense_data = ExpenseCreate(
            amount=Decimal(amount),
            description=description,
            expense_date=date.fromisoformat(expense_date),
            category_id=category_id,
            notes=notes
        )
        await ExpenseService.create_expense(db, expense_data)
        return RedirectResponse(url="/expenses", status_code=status.HTTP_303_SEE_OTHER)
    except (EntityNotFoundException, ValidationException) as e:
        categories = await CategoryService.get_all_categories(db)
        return templates.TemplateResponse("expenses/form.html", {
            "request": request,
            "categories": categories,
            "is_edit": False,
            "error": e.message,
            "amount": amount,
            "description": description,
            "expense_date": expense_date,
            "category_id": category_id,
            "notes": notes
        })
    except Exception as e:
        categories = await CategoryService.get_all_categories(db)
        return templates.TemplateResponse("expenses/form.html", {
            "request": request,
            "categories": categories,
            "is_edit": False,
            "error": f"Failed to create expense: {str(e)}",
            "amount": amount,
            "description": description,
            "expense_date": expense_date,
            "category_id": category_id,
            "notes": notes
        })

@router.get("/expenses/{expense_id}/edit", response_class=HTMLResponse)
async def edit_expense_form(request: Request, expense_id: int, db: AsyncSession = Depends(get_db)):
    """
    Show form to edit an existing expense.
    """
    try:
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        categories = await CategoryService.get_all_categories(db)
        return templates.TemplateResponse("expenses/form.html", {
            "request": request,
            "expense": expense,
            "categories": categories,
            "is_edit": True
        })
    except EntityNotFoundException as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": e.message
        })

@router.post("/expenses/{expense_id}/edit", response_class=RedirectResponse)
async def update_expense(
    request: Request,
    expense_id: int,
    amount: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    expense_date: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    notes: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Handle expense update form submission.
    """
    try:
        expense_data = ExpenseUpdate(
            amount=Decimal(amount) if amount else None,
            description=description,
            expense_date=date.fromisoformat(expense_date) if expense_date else None,
            category_id=category_id,
            notes=notes
        )
        await ExpenseService.update_expense(db, expense_id, expense_data)
        return RedirectResponse(url="/expenses", status_code=status.HTTP_303_SEE_OTHER)
    except (EntityNotFoundException, ValidationException) as e:
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        categories = await CategoryService.get_all_categories(db)
        return templates.TemplateResponse("expenses/form.html", {
            "request": request,
            "expense": expense,
            "categories": categories,
            "is_edit": True,
            "error": e.message
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Failed to update expense: {str(e)}"
        })

@router.post("/expenses/{expense_id}/delete", response_class=RedirectResponse)
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    """
    Handle expense deletion.
    """
    try:
        await ExpenseService.delete_expense(db, expense_id)
        return RedirectResponse(url="/expenses", status_code=status.HTTP_303_SEE_OTHER)
    except EntityNotFoundException:
        return RedirectResponse(url="/expenses", status_code=status.HTTP_303_SEE_OTHER)
