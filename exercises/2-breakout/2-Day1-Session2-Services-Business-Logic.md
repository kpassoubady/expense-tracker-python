# 🏗️ Day 1 - Session 2: Personal Expense Tracker - Services & Business Logic (45 mins)

## 🎯 Learning Objectives

By the end of this session, you will:

- Create service layer with comprehensive business logic
- Implement custom exceptions for proper error handling
- Add validation and data integrity checks
- Create unit tests for critical service methods
- Seed database with sample data for testing

**⏱️ Time Allocation: 45 minutes (with Q&A buffer)**

---

## 📋 Prerequisites Check (2 minutes)

- ✅ Session 1 completed successfully
- ✅ Models and schemas working
- ✅ Application starts without errors
- ✅ Database tables created

**Quick Test**: Verify your foundation is solid:

```bash
# Ensure app still starts
uvicorn app.main:app --reload

# Test imports work
python -c "from app.models import Category, Expense; print('✅ OK')"
```

---

## 🚀 Session Overview

In this session, we'll add the business logic layer that makes your expense tracker intelligent. We'll focus on essential services, error handling, and testing to ensure everything works reliably.

### 🎯 What You'll Build (45 minutes)

- **Custom Exceptions**: Professional error handling
- **Category Service**: CRUD operations with validation
- **Expense Service**: Business logic with category integration
- **Unit Tests**: Key service method testing
- **Data Seeding**: Sample data for development

---

## 📝 Step 1: Create Custom Exceptions (5 minutes)

### 🤖 Activate FastAPI Expert Mode

```text
@workspace /agents fastapi-expert

"We're moving to the service layer. Help me understand best practices for exception handling in FastAPI services."
```

### 🚨 Exception Classes

**Copilot Prompt:**

```text
/generate Create custom exception classes in app/exceptions.py:

1. AppException (base class):
   - message: str
   - status_code: int = 500
   - detail: Optional[dict] = None

2. EntityNotFoundException(AppException):
   - status_code = 404
   - Static method: not_found(entity_name: str, entity_id: int)

3. ValidationException(AppException):
   - status_code = 400
   - Static method: invalid_data(field: str, reason: str)

4. DuplicateEntityException(AppException):
   - status_code = 409
   - Static method: duplicate(entity_name: str, field: str, value: str)

Include proper __init__ methods and docstrings
```

**Expected file**: `app/exceptions.py`

```python
from typing import Optional, Dict, Any


class AppException(Exception):
    """Base exception for application errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        detail: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


class EntityNotFoundException(AppException):
    """Exception raised when an entity is not found."""
    
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, detail=detail)
    
    @staticmethod
    def not_found(entity_name: str, entity_id: int) -> "EntityNotFoundException":
        return EntityNotFoundException(
            message=f"{entity_name} with id {entity_id} not found",
            detail={"entity": entity_name, "id": entity_id}
        )


class ValidationException(AppException):
    """Exception raised for validation errors."""
    
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, detail=detail)
    
    @staticmethod
    def invalid_data(field: str, reason: str) -> "ValidationException":
        return ValidationException(
            message=f"Invalid {field}: {reason}",
            detail={"field": field, "reason": reason}
        )


class DuplicateEntityException(AppException):
    """Exception raised when attempting to create a duplicate entity."""
    
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=409, detail=detail)
    
    @staticmethod
    def duplicate(entity_name: str, field: str, value: str) -> "DuplicateEntityException":
        return DuplicateEntityException(
            message=f"{entity_name} with {field} '{value}' already exists",
            detail={"entity": entity_name, "field": field, "value": value}
        )
```

---

## 📝 Step 2: Create Category Service (12 minutes)

### 🏢 Category Service Implementation

**Copilot Prompt:**

```text
/generate Create CategoryService in app/services/category_service.py with:

Async CRUD operations using SQLAlchemy:
- get_all_categories(db: AsyncSession) -> List[Category]
- get_category_by_id(db: AsyncSession, category_id: int) -> Category
- get_category_by_name(db: AsyncSession, name: str) -> Optional[Category]
- create_category(db: AsyncSession, category_data: CategoryCreate) -> Category
- update_category(db: AsyncSession, category_id: int, category_data: CategoryUpdate) -> Category
- delete_category(db: AsyncSession, category_id: int) -> bool

Business methods:
- get_category_statistics(db: AsyncSession) -> Dict with usage stats
- get_categories_with_expense_count(db: AsyncSession) -> List[tuple]

Include:
- Duplicate name validation
- EntityNotFoundException for missing categories
- Proper async/await syntax
- Type hints throughout
- Logging for debugging
```

**Expected file**: `app/services/category_service.py`

```python
import logging
from typing import List, Optional, Dict, Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Category, Expense
from app.schemas import CategoryCreate, CategoryUpdate
from app.exceptions import EntityNotFoundException, DuplicateEntityException

logger = logging.getLogger(__name__)


class CategoryService:
    """Service class for Category operations."""

    @staticmethod
    async def get_all_categories(db: AsyncSession) -> List[Category]:
        """Get all categories ordered by name."""
        result = await db.execute(
            select(Category).order_by(Category.name)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_category_by_id(db: AsyncSession, category_id: int) -> Category:
        """Get category by ID or raise EntityNotFoundException."""
        result = await db.execute(
            select(Category).where(Category.id == category_id)
        )
        category = result.scalar_one_or_none()
        if not category:
            raise EntityNotFoundException.not_found("Category", category_id)
        return category

    @staticmethod
    async def get_category_by_name(db: AsyncSession, name: str) -> Optional[Category]:
        """Get category by name (case-insensitive)."""
        result = await db.execute(
            select(Category).where(func.lower(Category.name) == name.lower())
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_category(db: AsyncSession, category_data: CategoryCreate) -> Category:
        """Create a new category with duplicate validation."""
        # Check for duplicate name
        existing = await CategoryService.get_category_by_name(db, category_data.name)
        if existing:
            raise DuplicateEntityException.duplicate("Category", "name", category_data.name)

        category = Category(**category_data.model_dump())
        db.add(category)
        await db.flush()
        await db.refresh(category)
        logger.info(f"Created category: {category.name}")
        return category

    @staticmethod
    async def update_category(
        db: AsyncSession, 
        category_id: int, 
        category_data: CategoryUpdate
    ) -> Category:
        """Update an existing category."""
        category = await CategoryService.get_category_by_id(db, category_id)
        
        # Check for duplicate name if name is being changed
        update_dict = category_data.model_dump(exclude_unset=True)
        if "name" in update_dict and update_dict["name"] != category.name:
            existing = await CategoryService.get_category_by_name(db, update_dict["name"])
            if existing:
                raise DuplicateEntityException.duplicate("Category", "name", update_dict["name"])

        for field, value in update_dict.items():
            setattr(category, field, value)

        await db.flush()
        await db.refresh(category)
        logger.info(f"Updated category: {category.name}")
        return category

    @staticmethod
    async def delete_category(db: AsyncSession, category_id: int) -> bool:
        """Delete a category by ID."""
        category = await CategoryService.get_category_by_id(db, category_id)
        await db.delete(category)
        await db.flush()
        logger.info(f"Deleted category: {category.name}")
        return True

    @staticmethod
    async def get_category_count(db: AsyncSession) -> int:
        """Get total number of categories."""
        result = await db.execute(select(func.count(Category.id)))
        return result.scalar() or 0

    @staticmethod
    async def get_categories_with_expense_count(db: AsyncSession) -> List[Dict[str, Any]]:
        """Get all categories with their expense counts."""
        result = await db.execute(
            select(
                Category,
                func.count(Expense.id).label("expense_count")
            )
            .outerjoin(Expense)
            .group_by(Category.id)
            .order_by(Category.name)
        )
        
        return [
            {
                "category": row[0],
                "expense_count": row[1]
            }
            for row in result.all()
        ]
```

### ✅ **Quick Test**

```bash
python -c "from app.services.category_service import CategoryService; print('✅ CategoryService OK')"
```

---

## 📝 Step 3: Create Expense Service (12 minutes)

### 💼 Expense Service Implementation

**Copilot Prompt:**

```text
/generate Create ExpenseService in app/services/expense_service.py with:

Async CRUD operations:
- get_all_expenses(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Expense]
- get_expense_by_id(db: AsyncSession, expense_id: int) -> Expense
- create_expense(db: AsyncSession, expense_data: ExpenseCreate) -> Expense
- update_expense(db: AsyncSession, expense_id: int, expense_data: ExpenseUpdate) -> Expense
- delete_expense(db: AsyncSession, expense_id: int) -> bool

Query and reporting methods:
- get_expenses_by_category(db: AsyncSession, category_id: int) -> List[Expense]
- get_expenses_by_date_range(db: AsyncSession, start_date: date, end_date: date) -> List[Expense]
- get_total_expense_amount(db: AsyncSession) -> Decimal
- search_expenses(db: AsyncSession, keyword: str) -> List[Expense]
- get_expense_statistics(db: AsyncSession) -> Dict with stats

Business validation:
- Validate category exists before creating expense
- Validate amount is positive
- Validate date is not in future

Include async/await, type hints, logging
```

**Expected file**: `app/services/expense_service.py`

```python
import logging
from datetime import date
from decimal import Decimal
from typing import List, Optional, Dict, Any

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Expense, Category
from app.schemas import ExpenseCreate, ExpenseUpdate
from app.exceptions import EntityNotFoundException, ValidationException

logger = logging.getLogger(__name__)


class ExpenseService:
    """Service class for Expense operations."""

    @staticmethod
    async def get_all_expenses(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Expense]:
        """Get all expenses with pagination, ordered by date descending."""
        result = await db.execute(
            select(Expense)
            .options(selectinload(Expense.category))
            .order_by(Expense.expense_date.desc(), Expense.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_expense_by_id(db: AsyncSession, expense_id: int) -> Expense:
        """Get expense by ID or raise EntityNotFoundException."""
        result = await db.execute(
            select(Expense)
            .options(selectinload(Expense.category))
            .where(Expense.id == expense_id)
        )
        expense = result.scalar_one_or_none()
        if not expense:
            raise EntityNotFoundException.not_found("Expense", expense_id)
        return expense

    @staticmethod
    async def create_expense(db: AsyncSession, expense_data: ExpenseCreate) -> Expense:
        """Create a new expense with validation."""
        # Validate category exists
        category_result = await db.execute(
            select(Category).where(Category.id == expense_data.category_id)
        )
        if not category_result.scalar_one_or_none():
            raise ValidationException.invalid_data(
                "category_id", 
                f"Category with id {expense_data.category_id} does not exist"
            )

        # Validate amount
        if expense_data.amount <= 0:
            raise ValidationException.invalid_data("amount", "Amount must be positive")

        # Validate date
        if expense_data.expense_date > date.today():
            raise ValidationException.invalid_data(
                "expense_date", 
                "Expense date cannot be in the future"
            )

        expense = Expense(**expense_data.model_dump())
        db.add(expense)
        await db.flush()
        await db.refresh(expense)
        
        # Load category relationship
        result = await db.execute(
            select(Expense)
            .options(selectinload(Expense.category))
            .where(Expense.id == expense.id)
        )
        expense = result.scalar_one()
        
        logger.info(f"Created expense: {expense.description} - ${expense.amount}")
        return expense

    @staticmethod
    async def update_expense(
        db: AsyncSession, 
        expense_id: int, 
        expense_data: ExpenseUpdate
    ) -> Expense:
        """Update an existing expense."""
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        
        update_dict = expense_data.model_dump(exclude_unset=True)
        
        # Validate category if being updated
        if "category_id" in update_dict:
            category_result = await db.execute(
                select(Category).where(Category.id == update_dict["category_id"])
            )
            if not category_result.scalar_one_or_none():
                raise ValidationException.invalid_data(
                    "category_id", 
                    f"Category with id {update_dict['category_id']} does not exist"
                )

        for field, value in update_dict.items():
            setattr(expense, field, value)

        await db.flush()
        await db.refresh(expense)
        logger.info(f"Updated expense: {expense.description}")
        return expense

    @staticmethod
    async def delete_expense(db: AsyncSession, expense_id: int) -> bool:
        """Delete an expense by ID."""
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        await db.delete(expense)
        await db.flush()
        logger.info(f"Deleted expense: {expense.description}")
        return True

    @staticmethod
    async def get_expenses_by_category(
        db: AsyncSession, 
        category_id: int
    ) -> List[Expense]:
        """Get all expenses for a specific category."""
        result = await db.execute(
            select(Expense)
            .options(selectinload(Expense.category))
            .where(Expense.category_id == category_id)
            .order_by(Expense.expense_date.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_expenses_by_date_range(
        db: AsyncSession, 
        start_date: date, 
        end_date: date
    ) -> List[Expense]:
        """Get expenses within a date range."""
        result = await db.execute(
            select(Expense)
            .options(selectinload(Expense.category))
            .where(
                and_(
                    Expense.expense_date >= start_date,
                    Expense.expense_date <= end_date
                )
            )
            .order_by(Expense.expense_date.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_total_expense_amount(db: AsyncSession) -> Decimal:
        """Get sum of all expense amounts."""
        result = await db.execute(
            select(func.coalesce(func.sum(Expense.amount), 0))
        )
        return Decimal(str(result.scalar() or 0))

    @staticmethod
    async def get_expense_count(db: AsyncSession) -> int:
        """Get total number of expenses."""
        result = await db.execute(select(func.count(Expense.id)))
        return result.scalar() or 0

    @staticmethod
    async def search_expenses(db: AsyncSession, keyword: str) -> List[Expense]:
        """Search expenses by description keyword."""
        result = await db.execute(
            select(Expense)
            .options(selectinload(Expense.category))
            .where(Expense.description.ilike(f"%{keyword}%"))
            .order_by(Expense.expense_date.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_spending_by_category(db: AsyncSession) -> List[Dict[str, Any]]:
        """Get total spending grouped by category."""
        result = await db.execute(
            select(
                Category.name,
                Category.color,
                func.coalesce(func.sum(Expense.amount), 0).label("total")
            )
            .outerjoin(Expense)
            .group_by(Category.id, Category.name, Category.color)
            .order_by(func.sum(Expense.amount).desc())
        )
        return [
            {"name": row[0], "color": row[1], "total": float(row[2])}
            for row in result.all()
        ]
```

### 🔧 Update Services __init__.py

```python
from app.services.category_service import CategoryService
from app.services.expense_service import ExpenseService

__all__ = ["CategoryService", "ExpenseService"]
```

---

## 📝 Step 4: Create Sample Data Seeder (8 minutes)

### 🌱 Data Seeding Component

**Copilot Prompt:**

```text
/generate Create data seeder in app/seed_data.py with:

Async function seed_database(db: AsyncSession) that:
- Creates 6 sample categories (Food, Transport, Entertainment, Shopping, Bills, Health)
- Each category has appropriate FontAwesome icon and color code
- Generates 15-20 realistic expenses across different categories
- Uses various amounts ($5-$500) and recent dates (last 30 days)
- Includes realistic descriptions
- Checks if data already exists before seeding
- Logs all seeding activities

Sample categories:
- Food: icon "fas fa-utensils", color "#FF6B6B"
- Transport: icon "fas fa-car", color "#4ECDC4"  
- Entertainment: icon "fas fa-film", color "#45B7D1"
- Shopping: icon "fas fa-shopping-bag", color "#96CEB4"
- Bills: icon "fas fa-file-invoice", color "#FECA57"
- Health: icon "fas fa-medkit", color "#FF9FF3"
```

**Expected file**: `app/seed_data.py`

```python
import logging
import random
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category, Expense

logger = logging.getLogger(__name__)

SAMPLE_CATEGORIES = [
    {"name": "Food", "description": "Food and dining expenses", "icon": "fas fa-utensils", "color": "#FF6B6B"},
    {"name": "Transport", "description": "Transportation costs", "icon": "fas fa-car", "color": "#4ECDC4"},
    {"name": "Entertainment", "description": "Entertainment and leisure", "icon": "fas fa-film", "color": "#45B7D1"},
    {"name": "Shopping", "description": "Shopping and retail", "icon": "fas fa-shopping-bag", "color": "#96CEB4"},
    {"name": "Bills", "description": "Bills and utilities", "icon": "fas fa-file-invoice", "color": "#FECA57"},
    {"name": "Health", "description": "Healthcare expenses", "icon": "fas fa-medkit", "color": "#FF9FF3"},
]

SAMPLE_EXPENSES = {
    "Food": [
        ("Grocery shopping", 85.50, 150.00),
        ("Restaurant dinner", 45.00, 120.00),
        ("Coffee shop", 5.00, 15.00),
        ("Fast food lunch", 10.00, 25.00),
    ],
    "Transport": [
        ("Gas station", 40.00, 80.00),
        ("Uber ride", 15.00, 45.00),
        ("Parking fee", 5.00, 20.00),
        ("Car wash", 15.00, 35.00),
    ],
    "Entertainment": [
        ("Movie tickets", 15.00, 35.00),
        ("Streaming subscription", 10.00, 20.00),
        ("Concert tickets", 50.00, 150.00),
        ("Video game", 30.00, 70.00),
    ],
    "Shopping": [
        ("Clothing purchase", 50.00, 200.00),
        ("Electronics", 100.00, 500.00),
        ("Home supplies", 25.00, 100.00),
        ("Books", 15.00, 50.00),
    ],
    "Bills": [
        ("Electricity bill", 80.00, 150.00),
        ("Internet bill", 50.00, 80.00),
        ("Phone bill", 40.00, 100.00),
        ("Insurance payment", 100.00, 300.00),
    ],
    "Health": [
        ("Pharmacy purchase", 20.00, 80.00),
        ("Doctor visit copay", 25.00, 50.00),
        ("Gym membership", 30.00, 60.00),
        ("Vitamins", 15.00, 40.00),
    ],
}


async def seed_database(db: AsyncSession) -> None:
    """Seed the database with sample data if empty."""
    
    # Check if data already exists
    result = await db.execute(select(func.count(Category.id)))
    category_count = result.scalar() or 0
    
    if category_count > 0:
        logger.info(f"Database already has {category_count} categories. Skipping seed.")
        return

    logger.info("🌱 Starting database seeding...")

    # Create categories
    categories = {}
    for cat_data in SAMPLE_CATEGORIES:
        category = Category(**cat_data)
        db.add(category)
        await db.flush()
        categories[cat_data["name"]] = category
        logger.info(f"  Created category: {category.name}")

    # Create expenses
    expense_count = 0
    today = date.today()
    
    for category_name, expense_templates in SAMPLE_EXPENSES.items():
        category = categories[category_name]
        
        # Create 2-4 expenses per category
        for _ in range(random.randint(2, 4)):
            template = random.choice(expense_templates)
            description, min_amount, max_amount = template
            
            expense = Expense(
                description=description,
                amount=Decimal(str(round(random.uniform(min_amount, max_amount), 2))),
                expense_date=today - timedelta(days=random.randint(0, 30)),
                category_id=category.id
            )
            db.add(expense)
            expense_count += 1

    await db.flush()
    logger.info(f"✅ Seeding complete: {len(categories)} categories, {expense_count} expenses")
```

### 🔧 Update main.py to Include Seeding

Update `app/main.py` lifespan (note: check your method name may be different than create_tables()):

```python
from app.seed_data import seed_database
from app.database import async_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("✅ Database tables created")
    
    # Seed sample data
    async with async_session() as db:
        await seed_database(db)
        await db.commit()
    
    yield
    print("👋 Application shutting down")
```

---

## 📝 Step 5: Create Essential Tests (5 minutes)

### 🧪 Basic Service Tests

**Copilot Prompt:**

```text
/generate Create tests/test_services.py with pytest tests:

Test CategoryService:
- test_create_category() - verify category creation
- test_create_duplicate_category() - verify duplicate name raises exception
- test_get_category_by_id() - verify retrieval
- test_get_category_not_found() - verify exception for missing

Test ExpenseService:
- test_create_expense() - verify expense creation with category
- test_create_expense_invalid_category() - verify validation
- test_get_expenses_by_category() - verify filtering

Use pytest-asyncio, fixtures for database session
```

**Expected file**: `tests/test_services.py`

```python
import pytest
from decimal import Decimal
from datetime import date

from app.models import Category, Expense
from app.schemas import CategoryCreate, ExpenseCreate
from app.services import CategoryService, ExpenseService
from app.exceptions import EntityNotFoundException, DuplicateEntityException, ValidationException


@pytest.mark.asyncio
async def test_create_category(db_session):
    """Test creating a new category."""
    category_data = CategoryCreate(
        name="Test Category",
        description="Test Description",
        icon="fas fa-test",
        color="#123456"
    )
    
    category = await CategoryService.create_category(db_session, category_data)
    
    assert category.id is not None
    assert category.name == "Test Category"
    assert category.color == "#123456"


@pytest.mark.asyncio
async def test_create_duplicate_category(db_session):
    """Test that duplicate category names raise exception."""
    category_data = CategoryCreate(name="Duplicate Test")
    
    await CategoryService.create_category(db_session, category_data)
    
    with pytest.raises(DuplicateEntityException):
        await CategoryService.create_category(db_session, category_data)


@pytest.mark.asyncio
async def test_get_category_by_id(db_session):
    """Test retrieving category by ID."""
    category_data = CategoryCreate(name="Retrieve Test")
    created = await CategoryService.create_category(db_session, category_data)
    
    retrieved = await CategoryService.get_category_by_id(db_session, created.id)
    
    assert retrieved.id == created.id
    assert retrieved.name == "Retrieve Test"


@pytest.mark.asyncio
async def test_get_category_not_found(db_session):
    """Test that missing category raises EntityNotFoundException."""
    with pytest.raises(EntityNotFoundException):
        await CategoryService.get_category_by_id(db_session, 99999)


@pytest.mark.asyncio
async def test_create_expense(db_session):
    """Test creating a new expense."""
    # First create a category
    category = await CategoryService.create_category(
        db_session, 
        CategoryCreate(name="Expense Test Category")
    )
    
    expense_data = ExpenseCreate(
        amount=Decimal("50.00"),
        description="Test Expense",
        expense_date=date.today(),
        category_id=category.id
    )
    
    expense = await ExpenseService.create_expense(db_session, expense_data)
    
    assert expense.id is not None
    assert expense.amount == Decimal("50.00")
    assert expense.category_id == category.id


@pytest.mark.asyncio
async def test_create_expense_invalid_category(db_session):
    """Test that invalid category raises ValidationException."""
    expense_data = ExpenseCreate(
        amount=Decimal("50.00"),
        description="Invalid Category Test",
        expense_date=date.today(),
        category_id=99999
    )
    
    with pytest.raises(ValidationException):
        await ExpenseService.create_expense(db_session, expense_data)
```

### 🔧 Create Test Configuration

Create `tests/conftest.py`:

```python
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.database import Base


@pytest_asyncio.fixture
async def db_session():
    """Create a test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
        await session.rollback()
    
    await engine.dispose()
```

---

## 📝 Step 6: Testing & Verification (3 minutes)

### 🧪 Run Everything

```bash
python3 --version
pip3 --version
pip3 install --upgrade pip

pip3 install pytest
pip3 install pytest-asyncio
pip3 install fastapi httpx
pytest --version

# Run tests
pytest tests/ -v

# Start application and check seeding
uvicorn app.main:app --reload
```

### ✅ Verify Sample Data

Check logs for seeding confirmation:

```
🌱 Starting database seeding...
  Created category: Food
  Created category: Transport
  ...
✅ Seeding complete: 6 categories, 18 expenses
```

Optional: 
```bash
brew install sqlite
```
Validate the sample data:

```bash
sqlite3 expense_tracker.db "SELECT * FROM categories;"
sqlite3 expense_tracker.db "SELECT * FROM expenses LIMIT 5;"
```

You can also use the SQLite Browser or SQLite Viewer VSCode extension to view the database.

---

## 🎉 Session 2 Deliverables

### ✅ What You've Accomplished

- **✅ 3 Custom Exception Classes** for professional error handling
- **✅ CategoryService** with full CRUD and business logic
- **✅ ExpenseService** with validation and reporting methods
- **✅ Data Seeder** with realistic sample data
- **✅ 6+ Unit Tests** covering critical business logic

### 🔍 Quality Checklist

- [ ] All tests pass successfully
- [ ] Application starts and seeds data automatically
- [ ] Services handle validation and exceptions properly
- [ ] Logs confirm seeding operations completed
- [ ] No import errors or warnings

---

## 🎯 What's Next?

**Coming in Session 3**: REST APIs & Routes

- Create category and expense API routes
- Build JSON APIs with proper HTTP status codes
- Add request/response validation
- Test APIs with curl or Swagger UI

---

## 💡 GitHub Copilot Tips for This Session

### 🎯 Effective Prompts Used

```text
/generate Create [service class] with [specific async methods]
/test Generate pytest tests for [specific functionality]
/fix Fix the [specific error or issue]
```

### 🔧 Best Practices Learned

- **Service Layer**: Focus on business logic, not data access details
- **Exception Handling**: Use custom exceptions for domain-specific errors  
- **Async/Await**: Proper async patterns for database operations
- **Testing**: Test business rules, not just basic CRUD operations

---

## 🎊 Celebration Checkpoint

**What You've Built So Far:**

- ✅ **Complete Data Layer**: Models, schemas, relationships
- ✅ **Business Logic Layer**: Services with validation and error handling  
- ✅ **Sample Data**: 6 categories, 15+ realistic expenses
- ✅ **Quality Assurance**: Unit tests covering critical paths

**This is real, production-quality backend code!** 🚀
