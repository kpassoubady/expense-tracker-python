import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.database import Base
from app.services.category_service import CategoryService
from app.services.expense_service import ExpenseService
from app.schemas.category import CategoryCreate
from app.schemas.expense import ExpenseCreate
from app.exceptions import (
    DuplicateEntityException,
    EntityNotFoundException,
    ValidationException,
)
from datetime import date
from decimal import Decimal

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def db():
    engine = create_async_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_category(db):
    data = CategoryCreate(
        name="TestCat", description="desc", icon="icon", color="#123456"
    )
    category = await CategoryService.create_category(db, data)
    assert category.id is not None
    assert category.name == "TestCat"


@pytest.mark.asyncio
async def test_create_duplicate_category(db):
    data = CategoryCreate(
        name="DupCat", description="desc", icon="icon", color="#654321"
    )
    await CategoryService.create_category(db, data)
    with pytest.raises(DuplicateEntityException):
        await CategoryService.create_category(db, data)


@pytest.mark.asyncio
async def test_get_category_by_id(db):
    data = CategoryCreate(
        name="FindCat", description="desc", icon="icon", color="#abcdef"
    )
    category = await CategoryService.create_category(db, data)
    found = await CategoryService.get_category_by_id(db, category.id)
    assert found.id == category.id
    assert found.name == "FindCat"


@pytest.mark.asyncio
async def test_get_category_not_found(db):
    with pytest.raises(EntityNotFoundException):
        await CategoryService.get_category_by_id(db, 9999)


@pytest.mark.asyncio
async def test_create_expense(db):
    cat = await CategoryService.create_category(
        db,
        CategoryCreate(
            name="ExpenseCat", description="desc", icon="icon", color="#111111"
        ),
    )
    data = ExpenseCreate(
        amount=Decimal("25.50"),
        description="Lunch",
        expense_date=date.today(),
        category_id=cat.id,
        notes="Had a sandwich",
    )
    expense = await ExpenseService.create_expense(db, data)
    assert expense.id is not None
    assert expense.amount == Decimal("25.50")
    assert expense.category_id == cat.id
    assert expense.notes == "Had a sandwich"


@pytest.mark.asyncio
async def test_create_expense_invalid_category(db):
    data = ExpenseCreate(
        amount=Decimal("10.00"),
        description="InvalidCat",
        expense_date=date.today(),
        category_id=9999,
        notes="Invalid category test",
    )

    with pytest.raises(EntityNotFoundException):
        await ExpenseService.create_expense(db, data)


@pytest.mark.asyncio
async def test_get_expenses_by_category(db):
    cat = await CategoryService.create_category(
        db,
        CategoryCreate(
            name="FilterCat", description="desc", icon="icon", color="#222222"
        ),
    )
    await ExpenseService.create_expense(
        db,
        ExpenseCreate(
            amount=Decimal("10.00"),
            description="A",
            expense_date=date.today(),
            category_id=cat.id,
            notes="Note A",
        ),
    )
    await ExpenseService.create_expense(
        db,
        ExpenseCreate(
            amount=Decimal("20.00"),
            description="B",
            expense_date=date.today(),
            category_id=cat.id,
            notes="Note B",
        ),
    )
    expenses = await ExpenseService.get_expenses_by_category(db, cat.id)
    assert len(expenses) == 2
    for exp in expenses:
        assert exp.category_id == cat.id
