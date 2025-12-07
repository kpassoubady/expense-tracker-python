import logging
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.exceptions import EntityNotFoundException, ValidationException

logger = logging.getLogger(__name__)


class ExpenseService:
    @staticmethod
    async def get_all_expenses(
        db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Expense]:
        logger.debug(f"Fetching all expenses (skip={skip}, limit={limit})")
        result = await db.execute(select(Expense).offset(skip).limit(limit))
        return list(result.scalars().all())

    @staticmethod
    async def get_expense_by_id(db: AsyncSession, expense_id: int) -> Expense:
        logger.debug(f"Fetching expense by id: {expense_id}")
        expense = await db.get(Expense, expense_id)
        if not expense:
            logger.warning(f"Expense id {expense_id} not found")
            raise EntityNotFoundException.not_found("Expense", expense_id)
        return expense

    @staticmethod
    async def create_expense(db: AsyncSession, expense_data: ExpenseCreate) -> Expense:
        logger.debug(f"Creating expense: {expense_data}")
        # Validate category exists
        category = await db.get(Category, expense_data.category_id)
        if not category:
            logger.warning(
                f"Category id {expense_data.category_id} not found for expense creation"
            )
            raise EntityNotFoundException.not_found(
                "Category", expense_data.category_id
            )
        # Validate amount
        if expense_data.amount <= 0:
            logger.warning(f"Invalid expense amount: {expense_data.amount}")
            raise ValidationException.invalid_data("amount", "must be positive")
        # Validate date
        if expense_data.expense_date > date.today():
            logger.warning(f"Expense date {expense_data.expense_date} is in the future")
            raise ValidationException.invalid_data(
                "expense_date", "cannot be in the future"
            )
        expense = Expense(**expense_data.model_dump())
        db.add(expense)
        await db.commit()
        await db.refresh(expense)
        return expense

    @staticmethod
    async def update_expense(
        db: AsyncSession, expense_id: int, expense_data: ExpenseUpdate
    ) -> Expense:
        logger.debug(f"Updating expense id: {expense_id}")
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        update_data = expense_data.model_dump(exclude_unset=True)
        # Validate category if changed
        if "category_id" in update_data:
            category = await db.get(Category, update_data["category_id"])
            if not category:
                logger.warning(
                    f"Category id {update_data['category_id']} not found for expense update"
                )
                raise EntityNotFoundException.not_found(
                    "Category", update_data["category_id"]
                )
        # Validate amount if changed
        if "amount" in update_data and update_data["amount"] <= 0:
            logger.warning(f"Invalid expense amount: {update_data['amount']}")
            raise ValidationException.invalid_data("amount", "must be positive")
        # Validate date if changed
        if "expense_date" in update_data and update_data["expense_date"] > date.today():
            logger.warning(
                f"Expense date {update_data['expense_date']} is in the future"
            )
            raise ValidationException.invalid_data(
                "expense_date", "cannot be in the future"
            )
        for key, value in update_data.items():
            setattr(expense, key, value)
        await db.commit()
        await db.refresh(expense)
        return expense

    @staticmethod
    async def delete_expense(db: AsyncSession, expense_id: int) -> bool:
        logger.debug(f"Deleting expense id: {expense_id}")
        expense = await ExpenseService.get_expense_by_id(db, expense_id)
        await db.delete(expense)
        await db.commit()
        return True

    @staticmethod
    async def get_expenses_by_category(
        db: AsyncSession, category_id: int
    ) -> List[Expense]:
        logger.debug(f"Fetching expenses by category id: {category_id}")
        result = await db.execute(
            select(Expense).where(Expense.category_id == category_id)
        )
        return list(result.scalars().all()) 

    @staticmethod
    async def get_expenses_by_date_range(
        db: AsyncSession, start_date: date, end_date: date
    ) -> List[Expense]:
        logger.debug(f"Fetching expenses from {start_date} to {end_date}")
        result = await db.execute(
            select(Expense).where(
                and_(
                    Expense.expense_date >= start_date, Expense.expense_date <= end_date
                )
            )
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_total_expense_amount(db: AsyncSession) -> Decimal:
        logger.debug("Calculating total expense amount")
        result = await db.execute(select(func.coalesce(func.sum(Expense.amount), 0)))
        total = result.scalar_one()
        return Decimal(total)

    @staticmethod
    async def search_expenses(db: AsyncSession, keyword: str) -> List[Expense]:
        logger.debug(f"Searching expenses with keyword: {keyword}")
        result = await db.execute(
            select(Expense).where(or_(Expense.description.ilike(f"%{keyword}%")))
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_expense_statistics(db: AsyncSession) -> Dict[str, int]:
        logger.debug("Getting expense statistics")
        total_result = await db.execute(
            select(func.count(Expense.id).label("total_expenses"))
        )
        total = total_result.first()
        return {"total_expenses": total.total_expenses if total else 0}
