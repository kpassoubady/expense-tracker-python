from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.config import get_settings
from app.database import create_all_tables, dispose_engine, AsyncSessionLocal
from app.seed_data import seed_database
from app.routes.category_routes import router as category_router
from app.routes.expense_routes import router as expense_router
from app.routes.web_routes import router as web_router
import os

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    await create_all_tables()

    # Seed sample data
    async with AsyncSessionLocal() as db:
        await seed_database(db)
        await db.commit()

    yield
    # Shutdown: Dispose database engine
    print("👋 Application shutting down")
    await dispose_engine()


app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION, lifespan=lifespan)

# Include routers
app.include_router(category_router)
app.include_router(expense_router)
app.include_router(web_router)

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)

# Jinja2 templates setup
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_TITLE}!"}
