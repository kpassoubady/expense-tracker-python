# 🎨 Day 1 - Session 3: Personal Expense Tracker - REST APIs & Routes (45 mins)

## 🎯 Learning Objectives

By the end of this session, you will:

- Create REST API routes for Category and Expense operations
- Implement proper HTTP status codes and JSON responses
- Add request validation and error handling
- Test APIs with realistic data
- Master GitHub Copilot Chat Interface for API development

**⏱️ Time Allocation: 45 minutes (with Q&A buffer)**

---

## 📋 Prerequisites Check (2 minutes)

- ✅ Session 2 completed (services working)
- ✅ Application starts successfully with sample data
- ✅ Services work correctly (tested in previous session)
- ✅ Database contains categories and expenses

**Quick Test**: Verify your backend is ready:

```bash
# Start application
uvicorn app.main:app --reload

# Check health
curl http://localhost:8000/health
```

---

## 🚀 Session Overview

In this session, you'll expose your business logic through REST APIs. We'll create FastAPI routes that return JSON data, handle HTTP requests properly, and provide a foundation for frontend integration.

### 🎯 What You'll Build (45 minutes)

- **Category API Routes**: Full CRUD API with JSON responses
- **Expense API Routes**: Advanced querying and filtering APIs  
- **Error Handling**: Proper HTTP status codes and error messages
- **API Testing**: Verify all endpoints work correctly

---

## 📝 Step 1: Create API Response Models (5 minutes)

### 📋 Standard Response Schemas

**Copilot Prompt:**

```text
/generate Create app/schemas/response.py with standard API response models:

- ApiResponse[T]: Generic response with success, data, message fields
- PaginatedResponse[T]: Response with items, total, page, size fields
- ErrorResponse: Response with success=False, error, message, detail fields

Use Pydantic generics for type safety
Include examples in schema_extra
```

**Expected file**: `app/schemas/response.py`

```python
from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    data: Optional[T] = None
    message: str = "Success"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "data": {},
                "message": "Operation completed successfully"
            }
        }
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response."""
    success: bool = True
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "items": [],
                "total": 100,
                "page": 1,
                "size": 10,
                "pages": 10
            }
        }
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str
    message: str
    detail: Optional[Any] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error": "ValidationError",
                "message": "Invalid input data",
                "detail": {"field": "amount", "reason": "Must be positive"}
            }
        }
    )
```

---

## 📝 Step 2: Create Category API Routes (12 minutes)

### 🏷️ Category API Implementation

**Copilot Prompt:**

```text
/generate Create app/routes/category_routes.py with FastAPI router:

@router = APIRouter(prefix="/api/categories", tags=["Categories"])

Endpoints:
- GET /api/categories - return all categories with expense counts
- GET /api/categories/{id} - return single category or 404
- POST /api/categories - create new category with validation
- PUT /api/categories/{id} - update category
- DELETE /api/categories/{id} - delete with safety check

Additional endpoints:
- GET /api/categories/search?name={name} - search by name
- GET /api/categories/stats - return statistics

Include:
- Dependency injection for database session
- Proper HTTP status codes (200, 201, 400, 404, 409)
- Exception handling with try-except
- Type hints and docstrings
- Response models for Swagger documentation
```

**Expected file**: `app/routes/category_routes.py`

```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.response import ApiResponse, ErrorResponse
from app.services import CategoryService
from app.exceptions import EntityNotFoundException, DuplicateEntityException

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get(
    "",
    response_model=ApiResponse[List[CategoryResponse]],
    summary="Get all categories"
)
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all categories with expense counts."""
    categories_data = await CategoryService.get_categories_with_expense_count(db)
    
    result = []
    for item in categories_data:
        cat = item["category"]
        result.append(CategoryResponse(
            id=cat.id,
            name=cat.name,
            description=cat.description,
            icon=cat.icon,
            color=cat.color,
            created_at=cat.created_at,
            updated_at=cat.updated_at,
            expense_count=item["expense_count"]
        ))
    
    return ApiResponse(data=result, message=f"Found {len(result)} categories")


@router.get(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
    responses={404: {"model": ErrorResponse}}
)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific category by ID."""
    try:
        category = await CategoryService.get_category_by_id(db, category_id)
        expenses = await CategoryService.get_categories_with_expense_count(db)
        expense_count = next(
            (e["expense_count"] for e in expenses if e["category"].id == category_id), 
            0
        )
        
        return ApiResponse(
            data=CategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                icon=category.icon,
                color=category.color,
                created_at=category.created_at,
                updated_at=category.updated_at,
                expense_count=expense_count
            )
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post(
    "",
    response_model=ApiResponse[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
    responses={409: {"model": ErrorResponse}}
)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new category."""
    try:
        category = await CategoryService.create_category(db, category_data)
        return ApiResponse(
            data=CategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                icon=category.icon,
                color=category.color,
                created_at=category.created_at,
                updated_at=category.updated_at,
                expense_count=0
            ),
            message=f"Category '{category.name}' created successfully"
        )
    except DuplicateEntityException as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.put(
    "/{category_id}",
    response_model=ApiResponse[CategoryResponse],
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}}
)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing category."""
    try:
        category = await CategoryService.update_category(db, category_id, category_data)
        return ApiResponse(
            data=CategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                icon=category.icon,
                color=category.color,
                created_at=category.created_at,
                updated_at=category.updated_at,
                expense_count=0
            ),
            message=f"Category '{category.name}' updated successfully"
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except DuplicateEntityException as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.delete(
    "/{category_id}",
    response_model=ApiResponse[None],
    responses={404: {"model": ErrorResponse}}
)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a category by ID."""
    try:
        await CategoryService.delete_category(db, category_id)
        return ApiResponse(data=None, message="Category deleted successfully")
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get(
    "/search/",
    response_model=ApiResponse[List[CategoryResponse]]
)
async def search_categories(
    name: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    """Search categories by name."""
    category = await CategoryService.get_category_by_name(db, name)
    if category:
        return ApiResponse(
            data=[CategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                icon=category.icon,
                color=category.color,
                created_at=category.created_at,
                updated_at=category.updated_at,
                expense_count=0
            )],
            message="Category found"
        )
    return ApiResponse(data=[], message="No categories found")


@router.get("/stats/", response_model=ApiResponse[dict])
async def get_category_stats(db: AsyncSession = Depends(get_db)):
    """Get category statistics."""
    count = await CategoryService.get_category_count(db)
    categories = await CategoryService.get_categories_with_expense_count(db)
    
    return ApiResponse(
        data={
            "total_categories": count,
            "categories_with_expenses": sum(1 for c in categories if c["expense_count"] > 0),
            "total_expenses": sum(c["expense_count"] for c in categories)
        },
        message="Statistics retrieved"
    )
```

### ✅ **Quick API Test**

```bash
# Get all categories
curl http://localhost:8000/api/categories

# Get specific category
curl http://localhost:8000/api/categories/1

# Create new category
curl -X POST http://localhost:8000/api/categories \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Category","description":"API Test","icon":"fas fa-test","color":"#123456"}'
```

---

## 📝 Step 3: Create Expense API Routes (15 minutes)

### 💰 Expense API Implementation

**Copilot Prompt:**

```text
/generate Create app/routes/expense_routes.py with FastAPI router:

@router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

Core CRUD endpoints:
- GET /api/expenses - return all expenses with pagination (?page=1&size=10)
- GET /api/expenses/{id} - return single expense with category details
- POST /api/expenses - create expense with category validation
- PUT /api/expenses/{id} - update expense  
- DELETE /api/expenses/{id} - delete expense

Advanced query endpoints:
- GET /api/expenses/category/{categoryId} - expenses by category
- GET /api/expenses/search?keyword={text}&start_date={date}&end_date={date}
- GET /api/expenses/recent?limit={n} - recent expenses
- GET /api/expenses/summary - expense totals and statistics

Analytics endpoints:
- GET /api/expenses/analytics/category - spending by category
- GET /api/expenses/analytics/monthly - monthly spending trends

Include proper pagination, date handling, response models
```

**Expected file**: `app/routes/expense_routes.py`

```python
from datetime import date
from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.schemas.response import ApiResponse, PaginatedResponse, ErrorResponse
from app.services import ExpenseService
from app.exceptions import EntityNotFoundException, ValidationException

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


@router.get(
    "",
    response_model=PaginatedResponse[ExpenseResponse],
    summary="Get all expenses with pagination"
)
async def get_expenses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all expenses with pagination."""
    skip = (page - 1) * size
    expenses = await ExpenseService.get_all_expenses(db, skip=skip, limit=size)
    total = await ExpenseService.get_expense_count(db)
    
    items = [
        ExpenseResponse(
            id=e.id,
            amount=e.amount,
            description=e.description,
            expense_date=e.expense_date,
            category_id=e.category_id,
            category_name=e.category_name,
            created_at=e.created_at,
            updated_at=e.updated_at
        )
        for e in expenses
    ]
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get(
    "/{expense_id}",
    response_model=ApiResponse[ExpenseResponse],
    responses={404: {"model": ErrorResponse}}
)
async def get_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific expense by ID."""
    try:
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        return ApiResponse(
            data=ExpenseResponse(
                id=expense.id,
                amount=expense.amount,
                description=expense.description,
                expense_date=expense.expense_date,
                category_id=expense.category_id,
                category_name=expense.category_name,
                created_at=expense.created_at,
                updated_at=expense.updated_at
            )
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post(
    "",
    response_model=ApiResponse[ExpenseResponse],
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}}
)
async def create_expense(
    expense_data: ExpenseCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new expense."""
    try:
        expense = await ExpenseService.create_expense(db, expense_data)
        return ApiResponse(
            data=ExpenseResponse(
                id=expense.id,
                amount=expense.amount,
                description=expense.description,
                expense_date=expense.expense_date,
                category_id=expense.category_id,
                category_name=expense.category_name,
                created_at=expense.created_at,
                updated_at=expense.updated_at
            ),
            message=f"Expense '{expense.description}' created successfully"
        )
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.put(
    "/{expense_id}",
    response_model=ApiResponse[ExpenseResponse],
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing expense."""
    try:
        expense = await ExpenseService.update_expense(db, expense_id, expense_data)
        return ApiResponse(
            data=ExpenseResponse(
                id=expense.id,
                amount=expense.amount,
                description=expense.description,
                expense_date=expense.expense_date,
                category_id=expense.category_id,
                category_name=expense.category_name,
                created_at=expense.created_at,
                updated_at=expense.updated_at
            ),
            message="Expense updated successfully"
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete(
    "/{expense_id}",
    response_model=ApiResponse[None],
    responses={404: {"model": ErrorResponse}}
)
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an expense by ID."""
    try:
        await ExpenseService.delete_expense(db, expense_id)
        return ApiResponse(data=None, message="Expense deleted successfully")
    except EntityNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get(
    "/category/{category_id}",
    response_model=ApiResponse[List[ExpenseResponse]]
)
async def get_expenses_by_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all expenses for a specific category."""
    expenses = await ExpenseService.get_expenses_by_category(db, category_id)
    
    items = [
        ExpenseResponse(
            id=e.id,
            amount=e.amount,
            description=e.description,
            expense_date=e.expense_date,
            category_id=e.category_id,
            category_name=e.category_name,
            created_at=e.created_at,
            updated_at=e.updated_at
        )
        for e in expenses
    ]
    
    return ApiResponse(data=items, message=f"Found {len(items)} expenses")


@router.get("/search/", response_model=ApiResponse[List[ExpenseResponse]])
async def search_expenses(
    keyword: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    """Search expenses by keyword and/or date range."""
    if keyword:
        expenses = await ExpenseService.search_expenses(db, keyword)
    elif start_date and end_date:
        expenses = await ExpenseService.get_expenses_by_date_range(db, start_date, end_date)
    else:
        expenses = await ExpenseService.get_all_expenses(db)
    
    # Apply date filter if both keyword and dates provided
    if keyword and start_date and end_date:
        expenses = [
            e for e in expenses 
            if start_date <= e.expense_date <= end_date
        ]
    
    items = [
        ExpenseResponse(
            id=e.id,
            amount=e.amount,
            description=e.description,
            expense_date=e.expense_date,
            category_id=e.category_id,
            category_name=e.category_name,
            created_at=e.created_at,
            updated_at=e.updated_at
        )
        for e in expenses
    ]
    
    return ApiResponse(data=items, message=f"Found {len(items)} expenses")


@router.get("/recent/", response_model=ApiResponse[List[ExpenseResponse]])
async def get_recent_expenses(
    limit: int = Query(5, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get most recent expenses."""
    expenses = await ExpenseService.get_all_expenses(db, skip=0, limit=limit)
    
    items = [
        ExpenseResponse(
            id=e.id,
            amount=e.amount,
            description=e.description,
            expense_date=e.expense_date,
            category_id=e.category_id,
            category_name=e.category_name,
            created_at=e.created_at,
            updated_at=e.updated_at
        )
        for e in expenses
    ]
    
    return ApiResponse(data=items, message=f"Showing {len(items)} recent expenses")


@router.get("/summary/", response_model=ApiResponse[dict])
async def get_expense_summary(db: AsyncSession = Depends(get_db)):
    """Get expense summary statistics."""
    total_amount = await ExpenseService.get_total_expense_amount(db)
    total_count = await ExpenseService.get_expense_count(db)
    
    return ApiResponse(
        data={
            "total_amount": float(total_amount),
            "total_count": total_count,
            "average_expense": float(total_amount / total_count) if total_count > 0 else 0
        },
        message="Summary statistics retrieved"
    )


@router.get("/analytics/category/", response_model=ApiResponse[List[dict]])
async def get_spending_by_category(db: AsyncSession = Depends(get_db)):
    """Get spending breakdown by category."""
    data = await ExpenseService.get_spending_by_category(db)
    return ApiResponse(data=data, message="Category analytics retrieved")
```

---

## 📝 Step 4: Register Routes in Main App (3 minutes)

### 🔧 Update main.py

Add route imports and registration:

```python
# Add to app/main.py
from app.routes.category_routes import router as category_router
from app.routes.expense_routes import router as expense_router

# After app creation, register routers
app.include_router(category_router)
app.include_router(expense_router)
```

### 🔧 Update Routes __init__.py

```python
from app.routes.category_routes import router as category_router
from app.routes.expense_routes import router as expense_router

__all__ = ["category_router", "expense_router"]
```

---

## 📝 Step 5: API Testing & Verification (8 minutes)

### 🧪 Test Category APIs

```bash
# 1. Get all categories
curl http://localhost:8000/api/categories | python -m json.tool

# 2. Get category by ID
curl http://localhost:8000/api/categories/1 | python -m json.tool

# 3. Get category statistics
curl http://localhost:8000/api/categories/stats/ | python -m json.tool

# 4. Create new category
curl -X POST http://localhost:8000/api/categories \
  -H "Content-Type: application/json" \
  -d '{"name":"Travel","description":"Travel expenses","icon":"fas fa-plane","color":"#8E44AD"}' \
  | python -m json.tool
```

### 🧪 Test Expense APIs

```bash
# 1. Get all expenses (paginated)
curl "http://localhost:8000/api/expenses?page=1&size=5" | python -m json.tool

# 2. Get expenses by category
curl http://localhost:8000/api/expenses/category/1 | python -m json.tool

# 3. Get recent expenses
curl "http://localhost:8000/api/expenses/recent/?limit=5" | python -m json.tool

# 4. Get expense summary
curl http://localhost:8000/api/expenses/summary/ | python -m json.tool

# 5. Get spending analytics
curl http://localhost:8000/api/expenses/analytics/category/ | python -m json.tool

# 6. Create new expense
curl -X POST http://localhost:8000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{"description":"API Test Expense","amount":"25.99","expense_date":"2024-01-15","category_id":1}' \
  | python -m json.tool
```

### ✅ **Verify Swagger Documentation**

Open http://localhost:8000/docs to see:
- All API endpoints documented
- Request/response schemas
- Try-it-out functionality

---

## 🎉 Session 3 Deliverables

### ✅ What You've Accomplished

- **✅ Category API Routes** with 6+ REST endpoints
- **✅ Expense API Routes** with 8+ REST endpoints including analytics
- **✅ Proper HTTP Status Codes** (200, 201, 400, 404, 409)
- **✅ Swagger Documentation** auto-generated
- **✅ Pagination Support** for expense listings
- **✅ Search & Filtering** endpoints functional

### 🔍 Quality Checklist

- [ ] All API endpoints respond correctly
- [ ] Error handling returns proper HTTP status codes
- [ ] JSON responses follow consistent format
- [ ] Pagination works for expense listings
- [ ] Search and filtering endpoints function correctly
- [ ] Swagger UI shows all endpoints with documentation

---

## 🎯 What's Next?

**Coming in Session 4**: Web Interface & Templates

- Create Jinja2 templates for category and expense management
- Build responsive web forms with Bootstrap
- Add dashboard with charts and analytics
- Integrate AJAX for dynamic updates

---

## 💡 GitHub Copilot Tips for This Session

### 🎯 Effective Prompts Used

```text
/generate Create FastAPI router with [specific endpoints]
/api Generate API endpoint for [specific functionality]
@workspace "How should this API integrate with services?"
```

### 🔧 Best Practices Learned

- **REST Design**: Use proper HTTP verbs and status codes
- **Error Handling**: Consistent error response format across all APIs
- **Validation**: Use Pydantic for automatic request validation
- **Documentation**: FastAPI generates Swagger docs automatically

### 🚀 API Testing Tips

- Use curl for quick testing during development
- Test both success and error scenarios
- Verify JSON response structure consistency
- Check HTTP status codes match expectations
- Use `/docs` for interactive API testing

---

## ❓ Troubleshooting

**Common Questions:**

1. **Q**: "What's the difference between APIRouter and FastAPI app?"
   **A**: APIRouter is for modular routes; FastAPI app is the main application

2. **Q**: "When should I return 400 vs 422?"
   **A**: 400 for business validation errors, 422 for schema validation (Pydantic handles this)

3. **Q**: "How do I add authentication to APIs?"
   **A**: Use FastAPI's dependency injection with OAuth2 or JWT - covered in advanced sessions

---

## 🎊 Mid-Course Celebration

**What You've Built So Far:**

- ✅ **Complete Backend**: Models, schemas, services, REST APIs
- ✅ **Professional APIs**: 14+ REST endpoints with proper HTTP semantics
- ✅ **Error Handling**: Graceful error responses and validation
- ✅ **Sample Data**: Ready for frontend development
- ✅ **Documentation**: Auto-generated Swagger UI

**You're now ready to build any frontend - web, mobile, or desktop!** 🚀
