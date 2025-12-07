# 🏗️ Day 1 - Session 1: Personal Expense Tracker - Models & Database (45 mins)

## 🎯 Learning Objectives

By the end of this session, you will:

- Create FastAPI project structure with SQLAlchemy models
- Implement Pydantic schemas for data validation
- Set up SQLite database configuration
- Master GitHub Copilot interface and context selection
- Verify models and database work correctly

**⏱️ Time Allocation: 45 minutes (includes Copilot mastery)**

## 🤖 GitHub Copilot Focus: Basic Interface & Code Generation

**Today's Copilot Skills:**

- Interface basics (inline completions, chat, command palette)
- Context selection with `#selection`, `#editor`
- Model selection and basic prompting
- Code generation for models and schemas

📚 **Reference**: [Copilot Mastery Guide](../0-copilot-mastery-guide.md) for advanced techniques

---

## 📋 Prerequisites Check (2 minutes)

- ✅ Python 3.11+ installed
- ✅ Virtual environment activated
- ✅ Dependencies installed (FastAPI, SQLAlchemy, Pydantic)
- ✅ GitHub Copilot enabled and authenticated

**Quick Test**: Verify setup by running:

```bash
python --version
pip list | grep -E "fastapi|sqlalchemy|pydantic"
```

---

## 🚀 Session Overview

In this first session, you'll build the foundation data layer of the expense tracker. We'll focus on creating solid SQLAlchemy models and Pydantic schemas without rushing into complex business logic.

### 🎯 What You'll Build (45 minutes)

- **SQLAlchemy Models**: Category and Expense with relationships
- **Pydantic Schemas**: Request/response validation schemas
- **Database Config**: SQLite setup for development
- **Basic Validation**: Essential data validation

---

## 📝 Step 1: Project Setup & Configuration (8 minutes)

### 🔧 Check Current Project Structure

```bash
# Navigate to project directory
cd ~/projects/expense-tracker-python

# Activate virtual environment
source venv/bin/activate

# Check current structure
ls -la app/
```

### 📄 Verify Database Configuration

Check if `app/database.py` exists with proper async SQLAlchemy setup.

**GitHub Copilot Prompt:**

```text
@workspace Check app/database.py configuration and suggest any missing settings for async SQLAlchemy with SQLite
```

**🤖 Copilot Practice**: Try switching models and compare responses:

```text
# In Copilot Chat, try:
/model gpt-4-turbo
"What database configuration is missing for development?"

/model claude-3.5-sonnet  
"Review this SQLAlchemy setup and suggest improvements"
```

---

## 📝 Step 1.5: Create Specialized Development Assistants (8 minutes)

### 🤖 GitHub Copilot Chat-Modes Setup

#### 🐍 Create FastAPI Expert Assistant

Create `.github/chatmodes/fastapi-expert.chatmode.md`:

**Copilot Prompt:**

```text
/generate Create specialized GitHub Copilot chatmode for FastAPI development:

Filepath: .github/chatmodes/fastapi-expert.chatmode.md

Include YAML frontmatter with:
- description: 'FastAPI development specialist for this expense tracker project'
- tools: []

Specialized behavior for:
- Project Context: FastAPI + Python 3.11+, SQLAlchemy 2.0, Pydantic 2.0
- Package structure: app/ with models, schemas, services, routes
- Jinja2 templates, async SQLAlchemy, RESTful APIs

Expertise areas:
- SQLAlchemy model design with proper relationships
- Pydantic schema validation
- Service layer with async operations
- FastAPI route best practices
- Testing recommendations
```

Check the file for any missing settings or improvements. You will see the below warning message:

```
Chat modes have been renamed to agents. Please move this file to file:///Users/kangs/projects/expense-tracker-python/.github/agents/fastapi-expert.agent.md
```

Ask Copilot to move the file to the correct location.

```
/fix Chat modes have been renamed to agents. Please move this file to file:///Users/kangs/projects/expense-tracker-python/.github/agents/fastapi-expert.agent.md
```


#### 🚀 Immediate Application

**Test Your FastAPI Expert:**

```text
@workspace /chatmode fastapi-expert

"Help me design the Category SQLAlchemy model with proper relationships."
```

```text
@workspace /agents fastapi-expert "Design a SQLAlchemy Category model with id, name, and a one-to-many relationship to Product."
```

---

## 📝 Step 2: Create Category Model (10 minutes)

### 🏷️ Category SQLAlchemy Model

**Copilot Prompt:**

```text
/generate Create a SQLAlchemy Category model in app/models/category.py with:
- Integer id (primary key, auto-increment)
- String name (required, unique, max 100 characters)
- String description (optional, max 255 characters)
- String icon (max 50 characters for FontAwesome icons like "fas fa-utensils")
- String color (7 characters for hex color codes like "#FF5733")
- DateTime created_at, updated_at (automatic timestamps)
- One-to-many relationship with Expense model
- Use SQLAlchemy 2.0 syntax with Mapped types
- Add __repr__ method for debugging
```

**Expected file**: `app/models/category.py`

```python
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.expense import Expense


class Category(Base):
    """Category model for organizing expenses."""
    
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), default="fas fa-folder")
    color: Mapped[Optional[str]] = mapped_column(String(7), default="#6c757d")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    expenses: Mapped[List["Expense"]] = relationship(
        "Expense", back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"
```

**🤖 Advanced Copilot Practice**:

1. **Context Selection**: Select the entire model class, then ask:

```text
"Analyze #selection and suggest improvements for SQLAlchemy best practices"
```

2. **Agent Usage**:

```text
@workspace "How should this Category model fit into the overall project structure?"
```

### ✅ Verification Point

- Ensure the model has no syntax errors
- Check that SQLAlchemy types are correct
- Verify relationship is properly defined

---

## 📝 Step 3: Create Expense Model (10 minutes)

### 💰 Expense SQLAlchemy Model

**Copilot Prompt:**

```text
/generate Create a SQLAlchemy Expense model in app/models/expense.py with:
- Integer id (primary key, auto-increment)
- Decimal amount (required, precision 12, scale 2)
- String description (required, max 255 characters)
- Date expense_date (required, defaults to today)
- Integer category_id (foreign key to categories table)
- Many-to-one relationship with Category model
- DateTime created_at, updated_at (automatic timestamps)
- Use SQLAlchemy 2.0 syntax with Mapped types
```

**Expected file**: `app/models/expense.py`

```python
from datetime import datetime, date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, DateTime, Date, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.category import Category


class Expense(Base):
    """Expense model for tracking personal expenses."""
    
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    expense_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    category: Mapped["Category"] = relationship("Category", back_populates="expenses")

    @property
    def category_name(self) -> Optional[str]:
        return self.category.name if self.category else None

    def __repr__(self) -> str:
        return f"<Expense(id={self.id}, amount={self.amount}, description='{self.description}')>"
```

### 🔧 Update Models __init__.py

```python
from app.models.category import Category
from app.models.expense import Expense

__all__ = ["Category", "Expense"]
```

---

## 📝 Step 4: Create Pydantic Schemas (10 minutes)

### 📋 Category Schemas

**Copilot Prompt:**

```text
/generate Create Pydantic schemas in app/schemas/category.py with:
- CategoryBase: name (required), description (optional), icon (optional), color (optional)
- CategoryCreate: inherits CategoryBase
- CategoryUpdate: all fields optional
- CategoryResponse: includes id, created_at, updated_at, expense_count
- Use Pydantic v2 syntax with ConfigDict
- Add field validations (min/max length, regex for color)
```

**Expected file**: `app/schemas/category.py`

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    icon: Optional[str] = Field("fas fa-folder", max_length=50)
    color: Optional[str] = Field("#6c757d", max_length=7)

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        if v and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex code")
        return v


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    icon: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=7)


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    expense_count: int = 0

    model_config = ConfigDict(from_attributes=True)
```

### 📋 Expense Schemas

**Copilot Prompt:**

```text
/generate Create Pydantic schemas in app/schemas/expense.py with:
- ExpenseBase: amount (Decimal, positive), description (required), expense_date, category_id
- ExpenseCreate: inherits ExpenseBase
- ExpenseUpdate: all fields optional
- ExpenseResponse: includes id, created_at, updated_at, category_name
- Use Pydantic v2 syntax
```

**Expected file**: `app/schemas/expense.py`

```python
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExpenseBase(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    description: str = Field(..., min_length=1, max_length=255)
    expense_date: date = Field(default_factory=date.today)
    category_id: int = Field(..., gt=0)

    @field_validator("expense_date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Expense date cannot be in the future")
        return v


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    expense_date: Optional[date] = None
    category_id: Optional[int] = Field(None, gt=0)


class ExpenseResponse(ExpenseBase):
    id: int
    category_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

## 📝 Step 5: Testing & Verification (5 minutes)

### 🧪 Quick Syntax Test

```bash
# Test model imports
python -c "from app.models import Category, Expense; print('✅ Models import OK')"

# Test schema imports
python -c "from app.schemas import CategoryCreate, ExpenseCreate; print('✅ Schemas import OK')"
```

**🤖 Terminal Integration Practice**: If you see errors:

```text
"Fix this import error: #terminal_selection"
```

### 🚀 Start the Application

```bash
uvicorn app.main:app --reload
```

### ✅ Verify Database Tables

1. Check that application starts without errors
2. Database file `expense_tracker.db` should be created
3. Visit `/docs` to see API documentation

---

## 🎉 Session 1 Deliverables

### ✅ What You've Accomplished

- **✅ 2 SQLAlchemy Models** (Category, Expense) with proper relationships
- **✅ 4 Pydantic Schema Classes** for validation
- **✅ Working SQLite Database** with auto-generated tables
- **✅ Proper Type Hints** throughout
- **✅ Compilation Success** - no import errors

### 🔍 Quality Checklist

- [ ] Application starts without errors
- [ ] Models have proper relationships
- [ ] Schemas have validation rules
- [ ] Type hints are complete
- [ ] Database tables created

---

## 🎯 What's Next?

**Coming in Session 2**: Service Layer & Business Logic

- Create CategoryService and ExpenseService
- Implement validation and business rules  
- Add exception handling
- Create sample data and testing

---

## 💡 GitHub Copilot Tips for This Session

### 🎯 Advanced Techniques Learned

- **Context Selectors**: `#selection`, `#editor`, `#terminal_selection`
- **Agent Usage**: `@workspace`, `@terminal` for specialized help
- **Model Switching**: Compare responses from different available models

### 🚀 Quick Reference Card

```text
CONTEXT SELECTORS:
#selection - Selected code/text
#editor - Current file contents  
#terminal_selection - Selected terminal output

AGENTS FOR DAY 1:
@workspace - Project structure questions
@terminal - Build and compilation help
```

---

## ❓ Troubleshooting

**Common Questions:**

1. **Q**: "Why use Decimal for money amounts?"
   **A**: Ask Copilot: `/explain why Decimal is better than float for financial calculations`

2. **Q**: "What's the difference between Pydantic and SQLAlchemy models?"
   **A**: SQLAlchemy = database mapping, Pydantic = API validation

3. **Q**: "Why use async SQLAlchemy?"
   **A**: Better performance for concurrent web requests

**🎯 Ready for Session 2?** Take a quick break, then continue to the service layer!
