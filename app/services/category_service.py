import logging
from typing import List, Optional, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.exceptions import EntityNotFoundException, DuplicateEntityException

logger = logging.getLogger(__name__)


class CategoryService:
    @staticmethod
    async def get_all_categories(db: AsyncSession) -> List[Category]:
        logger.debug("Fetching all categories")
        result = await db.execute(select(Category))
        return result.scalars().all()

    @staticmethod
    async def get_category_by_id(db: AsyncSession, category_id: int) -> Category:
        logger.debug(f"Fetching category by id: {category_id}")
        category = await db.get(Category, category_id)
        if not category:
            logger.warning(f"Category id {category_id} not found")
            raise EntityNotFoundException.not_found("Category", category_id)
        return category

    @staticmethod
    async def get_category_by_name(db: AsyncSession, name: str) -> Optional[Category]:
        logger.debug(f"Fetching category by name: {name}")
        result = await db.execute(select(Category).where(Category.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_category(
        db: AsyncSession, category_data: CategoryCreate
    ) -> Category:
        logger.debug(f"Creating category: {category_data.name}")
        existing = await CategoryService.get_category_by_name(db, category_data.name)
        if existing:
            logger.warning(f"Duplicate category name: {category_data.name}")
            raise DuplicateEntityException.duplicate(
                "Category", "name", category_data.name
            )
        category = Category(**category_data.model_dump())
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def update_category(
        db: AsyncSession, category_id: int, category_data: CategoryUpdate
    ) -> Category:
        logger.debug(f"Updating category id: {category_id}")
        category = await CategoryService.get_category_by_id(db, category_id)
        update_data = category_data.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing = await CategoryService.get_category_by_name(
                db, update_data["name"]
            )
            if existing and existing.id != category_id:
                logger.warning(f"Duplicate category name: {update_data['name']}")
                raise DuplicateEntityException.duplicate(
                    "Category", "name", update_data["name"]
                )
        for key, value in update_data.items():
            setattr(category, key, value)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def delete_category(db: AsyncSession, category_id: int) -> bool:
        logger.debug(f"Deleting category id: {category_id}")
        category = await CategoryService.get_category_by_id(db, category_id)
        await db.delete(category)
        await db.commit()
        return True

    @staticmethod
    async def get_category_statistics(db: AsyncSession) -> Dict[str, int]:
        logger.debug("Getting category usage statistics")
        result = await db.execute(
            select(func.count(Category.id).label("total_categories"))
        )
        stats = result.first()
        return {"total_categories": stats.total_categories if stats else 0}

    @staticmethod
    async def get_categories_with_expense_count(
        db: AsyncSession,
    ) -> List[Tuple[Category, int]]:
        logger.debug("Getting categories with expense count")
        from app.models.expense import Expense

        result = await db.execute(
            select(Category, func.count(Expense.id).label("expense_count"))
            .outerjoin(Expense, Category.id == Expense.category_id)
            .group_by(Category.id)
        )
        return [(row[0], row[1]) for row in result.all()]
