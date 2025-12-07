import logging
import random
from datetime import datetime, timedelta, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.category import Category
from app.models.expense import Expense

logger = logging.getLogger(__name__)

CATEGORIES = [
    {"name": "Food", "icon": "fas fa-utensils", "color": "#FF6B6B", "description": "Groceries, restaurants, snacks"},
    {"name": "Transport", "icon": "fas fa-car", "color": "#4ECDC4", "description": "Public transport, fuel, taxi"},
    {"name": "Entertainment", "icon": "fas fa-film", "color": "#45B7D1", "description": "Movies, concerts, games"},
    {"name": "Shopping", "icon": "fas fa-shopping-bag", "color": "#96CEB4", "description": "Clothes, gifts, online shopping"},
    {"name": "Bills", "icon": "fas fa-file-invoice", "color": "#FECA57", "description": "Utilities, rent, subscriptions"},
    {"name": "Health", "icon": "fas fa-medkit", "color": "#FF9FF3", "description": "Medicine, doctor, gym"},
]

EXPENSE_DESCRIPTIONS = [
    "Lunch at cafe", "Bus ticket", "Movie night", "New shoes", "Electricity bill", "Pharmacy purchase",
    "Groceries", "Taxi ride", "Concert ticket", "Online shopping", "Water bill", "Doctor visit",
    "Dinner with friends", "Fuel refill", "Streaming subscription", "Gym membership", "Gift for friend",
    "Snack", "Train fare", "Game purchase"
]

async def seed_database(db: AsyncSession):
    logger.info("Starting database seeding...")
    # Check if categories already exist
    result = await db.execute(select(func.count(Category.id)))
    category_count = result.scalar_one()
    if category_count > 0:
        logger.info("Categories already exist. Skipping seeding.")
        return

    # Create categories
    category_objs = []
    for cat in CATEGORIES:
        category = Category(
            name=cat["name"],
            description=cat["description"],
            icon=cat["icon"],
            color=cat["color"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(category)
        category_objs.append(category)
        logger.info(f"Added category: {cat['name']}")
    await db.commit()
    # Refresh to get IDs
    for category in category_objs:
        await db.refresh(category)

    # Generate expenses
    expenses = []
    for _ in range(random.randint(15, 20)):
        category = random.choice(category_objs)
        amount = round(random.uniform(5, 500), 2)
        description = random.choice(EXPENSE_DESCRIPTIONS)
        days_ago = random.randint(0, 29)
        expense_date = date.today() - timedelta(days=days_ago)
        expense = Expense(
            amount=amount,
            description=description,
            expense_date=expense_date,
            category_id=category.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(expense)
        expenses.append(expense)
        logger.info(f"Added expense: ${amount} for {category.name} ({description}) on {expense_date}")
    await db.commit()
    logger.info(f"Seeded {len(category_objs)} categories and {len(expenses)} expenses.")
