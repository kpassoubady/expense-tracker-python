# 🔧 Python Track Setup - Day 1 Backend

## 🎯 Setup Overview

This guide will help you set up your development environment for the Python (FastAPI) track of the Personal Expense Tracker bootcamp.

**⏱️ Estimated Time**: 15-20 minutes

---

## 📋 Prerequisites

### Required Software

Before starting, ensure you have:

- ✅ **Python 3.11 or 3.12** installed
- ✅ **pip** package manager
- ✅ **VS Code** (recommended) with Python extension
- ✅ **GitHub Copilot** extension enabled and authenticated
- ✅ **Git** for version control

---

## 🔍 Step 1: Verify Python Installation

Open a terminal and run:

```bash
# Check Python version
python --version
# or
python3 --version

# Expected output: Python 3.11.x or Python 3.12.x
```

If Python is not installed or version is below 3.11:
- **macOS**: `brew install python@3.12`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3.12 python3.12-venv`

---

## 📁 Step 2: Create Project Structure

### Create Project Directory

```bash
# Create project directory
mkdir -p ~/projects/expense-tracker-python
cd ~/projects/expense-tracker-python

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

### Verify Virtual Environment

```bash
# You should see (venv) in your terminal prompt
which python  # Should point to venv/bin/python

# Upgrade pip
pip install --upgrade pip
```

---

## 📦 Step 3: Install Dependencies

### Create requirements.txt

Create `requirements.txt` with the following dependencies:

```text
# Web Framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0

# Database
sqlalchemy>=2.0.25
aiosqlite>=0.19.0

# Data Validation
pydantic>=2.5.0
pydantic-settings>=2.1.0

# Templates
jinja2>=3.1.3
python-multipart>=0.0.9

# Testing
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.26.0

# Development Tools
python-dotenv>=1.0.0
black>=24.9.1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Verify Installation

```bash
# Check FastAPI version
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"

# Check SQLAlchemy version
python -c "import sqlalchemy; print(f'SQLAlchemy version: {sqlalchemy.__version__}')"
```

---

## 📂 Step 4: Create Project Structure

### Directory Structure

Create the following structure:

```bash
expense-tracker-python/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── (entities will be created in Session 1)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── (Pydantic schemas will be created)
│   ├── services/
│   │   ├── __init__.py
│   │   └── (services will be created in Session 2)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── (routes will be created in Session 3)
│   ├── templates/
│   │   └── (Jinja2 templates will be created in Session 4)
│   └── static/
│       ├── css/
│       └── js/
├── tests/
│   ├── __init__.py
│   └── (tests will be created)
├── requirements.txt
├── .env
└── README.md
```

### Create Directory Structure

```bash
# Create directories
mkdir -p app/{models,schemas,services,routes,templates,static/{css,js}}
mkdir -p tests

# Create __init__.py files
touch app/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/routes/__init__.py
touch tests/__init__.py
```

---

## ⚙️ Step 5: Create Base Configuration

### Create app/config.py

**GitHub Copilot Prompt:**

```text
/generate Create FastAPI configuration file with:
- Settings class using pydantic-settings BaseSettings
- Database URL for SQLite (default: sqlite:///./expense_tracker.db)
- Debug mode setting
- App title and version settings
- Environment variable support with .env file
- lru_cache decorator for cached settings
```

**Expected file** (`app/config.py`):

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_title: str = "Personal Expense Tracker"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./expense_tracker.db"
    
    # API
    api_prefix: str = "/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
```

### Create app/database.py

**GitHub Copilot Prompt:**

```text
/generate Create app/database.py SQLAlchemy database configuration for FastAPI with:
- Async SQLite engine using aiosqlite
- Session factory with async support
- Base class for declarative models
- Dependency function for database sessions
- Function to create all tables
```

**Expected file** (`app/database.py`):

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Convert sqlite URL to async format
DATABASE_URL = settings.database_url.replace("sqlite://", "sqlite+aiosqlite://")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
    future=True
)

# Session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


async def get_db():
    """Dependency for database sessions."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### Create app/main.py

**GitHub Copilot Prompt:**

```text
/generate Create app/main.py FastAPI main application file with:
- FastAPI app instance with title and version from settings
- Lifespan context manager to create tables on startup
- Static files mounting for CSS/JS
- Jinja2 templates setup
- Health check endpoint at /health
- Root endpoint returning welcome message
```

**Expected file** (`app/main.py`):

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await create_tables()
    print("✅ Database tables created")
    yield
    # Shutdown
    print("👋 Application shutting down")


# Create FastAPI app
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_title}",
        "version": settings.app_version,
        "docs": "/docs"
    }
```

### Create .env file

```bash
# Create .env file
cat > .env << EOF
# Application Settings
APP_TITLE=Personal Expense Tracker
APP_VERSION=1.0.0
DEBUG=true

# Database
DATABASE_URL=sqlite:///./expense_tracker.db
EOF
```

---

## 🚀 Step 6: Test Your Setup

### Run the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verify Endpoints

Open your browser or use curl:

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# API documentation (Swagger UI)
# Open: http://localhost:8000/docs

# Alternative API docs (ReDoc)
# Open: http://localhost:8000/redoc
```

**Expected Response from /health:**

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## ✅ Setup Verification Checklist

Before starting Session 1, verify:

- [ ] Python 3.11+ installed and working
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (no errors)
- [ ] Project structure created correctly
- [ ] `uvicorn app.main:app --reload` starts without errors
- [ ] Health check endpoint returns status "healthy"
- [ ] Swagger UI accessible at `/docs`
- [ ] GitHub Copilot working in VS Code

---

## 🔧 IDE Setup (VS Code)

### Recommended Extensions

Install these VS Code extensions:

1. **Python** (Microsoft) - Python language support
2. **Pylance** - Python language server
3. **GitHub Copilot** - AI pair programmer
4. **GitHub Copilot Chat** - Chat interface
5. **Python Indent** - Better Python indentation

### VS Code Settings

Add to `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    "python.formatting.provider": "none",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter"
    }
}
```

---

## ❓ Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# Check pip list
pip list | grep fastapi
```

**2. "Permission denied" on database**
```bash
# Check file permissions
ls -la expense_tracker.db
# If needed, remove and restart
rm expense_tracker.db
```

**3. Port already in use**
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process or use different port
uvicorn app.main:app --reload --port 8001
```

**4. Copilot not suggesting**
- Check GitHub Copilot status in VS Code status bar
- Ensure you're authenticated
- Try reloading VS Code

---

## 🎯 Next Steps

**You're ready for Session 1!**

👉 Proceed to [Session 1: Models & Database](../2-breakout/1-Day1-Session1-Models-Database.md)

In Session 1, you'll:
- Create SQLAlchemy models for Category and Expense
- Define Pydantic schemas for validation
- Practice GitHub Copilot basics with entity generation

**Happy coding! 🚀**
