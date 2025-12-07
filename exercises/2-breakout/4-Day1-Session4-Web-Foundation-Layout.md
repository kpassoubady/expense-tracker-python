# 🎨 Day 1 - Session 4: Web Foundation & Layout (25 mins)

## 🎯 Learning Objectives

By the end of this session, you will:

- Create a responsive base layout template with Bootstrap
- Build reusable navigation and page structure
- Implement error handling templates
- Set up web routes with proper template rendering
- Understand the `is_edit` flag pattern for reusable forms

**⏱️ Time Allocation: 25 minutes**

---

## 📋 Prerequisites Check (2 minutes)

- ✅ Session 3 completed (REST APIs working)
- ✅ All REST endpoints tested and functional
- ✅ Sample data available in database

**Quick Test**: Verify your APIs are ready:

```bash
curl http://localhost:8000/api/categories
curl http://localhost:8000/api/expenses
```

---

## 🚀 Session Overview

In this session, you'll create the foundational templates that all other pages will build upon. This includes the base layout with navigation, error handling, and the web routes infrastructure.

### 🎯 What You'll Build

- **Base Layout Template**: Reusable page structure with sidebar navigation
- **Error Page Template**: User-friendly error display
- **Web Routes**: FastAPI routes for rendering pages
- **Template Infrastructure**: Jinja2 setup with proper error handling

---

## 📝 Step 1: Create Base Layout Template (8 minutes)

The base template is the foundation that ALL other templates will extend. It must be created FIRST.

### 🏗️ Base Layout with Navigation

**Copilot Prompt:**

```text
/generate Create app/templates/layout/base.html as a Jinja2 base template with:

HTML5 structure with Bootstrap 5 CDN and Font Awesome CDN
Responsive sidebar navigation (250px width) with:
- Brand logo "Expense Tracker" with wallet icon
- Nav links: Dashboard (/), Expenses (/expenses), Categories (/categories)
- Active state highlighting based on request.url.path
- Dark gradient background (#1e293b to #334155)

Mobile navigation:
- Collapsible navbar for mobile screens
- Same nav links as sidebar

Main content area:
- margin-left matching sidebar width
- Padding and background color #f8f9fa

Jinja2 blocks:
- {% block title %}{% endblock %}
- {% block content %}{% endblock %}
- {% block extra_css %}{% endblock %}
- {% block extra_js %}{% endblock %}

Include Bootstrap 5 JS bundle at the end
Custom CSS for sidebar styling, card borders, button colors
```

**Expected file**: `app/templates/layout/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Expense Tracker{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">
    
    <style>
        :root {
            --primary-color: #4F46E5;
            --sidebar-width: 250px;
        }
        
        body {
            min-height: 100vh;
            background-color: #f8f9fa;
        }
        
        /* Sidebar Styles */
        .sidebar {
            width: var(--sidebar-width);
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
            padding-top: 1rem;
            z-index: 1000;
        }
        
        .sidebar .nav-link {
            color: rgba(255, 255, 255, 0.8);
            padding: 0.75rem 1.5rem;
            margin: 0.25rem 0.75rem;
            border-radius: 0.5rem;
            transition: all 0.2s;
        }
        
        .sidebar .nav-link:hover,
        .sidebar .nav-link.active {
            color: #fff;
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        .sidebar .nav-link i {
            width: 24px;
        }
        
        /* Main Content */
        .main-content {
            margin-left: var(--sidebar-width);
            padding: 2rem;
        }
        
        /* Brand Logo */
        .brand-logo {
            color: #fff;
            font-size: 1.5rem;
            font-weight: 700;
            padding: 0 1.5rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1rem;
        }
        
        /* Card Styles */
        .card {
            border: none;
            border-radius: 0.75rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        /* Button Styles */
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-primary:hover {
            background-color: #4338CA;
            border-color: #4338CA;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
            }
            .main-content {
                margin-left: 0;
            }
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Sidebar Navigation (Desktop) -->
    <nav class="sidebar d-none d-md-block">
        <div class="brand-logo">
            <i class="fas fa-wallet me-2"></i>Expense Tracker
        </div>
        <ul class="nav flex-column">
            <li class="nav-item">
                <a class="nav-link {% if request.url.path == '/' %}active{% endif %}" href="/">
                    <i class="fas fa-home me-2"></i>Dashboard
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if '/expenses' in request.url.path %}active{% endif %}" href="/expenses">
                    <i class="fas fa-receipt me-2"></i>Expenses
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link {% if '/categories' in request.url.path %}active{% endif %}" href="/categories">
                    <i class="fas fa-tags me-2"></i>Categories
                </a>
            </li>
        </ul>
    </nav>

    <!-- Mobile Navigation -->
    <nav class="navbar navbar-dark bg-dark d-md-none">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="fas fa-wallet me-2"></i>Expense Tracker
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mobileNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="mobileNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/"><i class="fas fa-home me-2"></i>Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/expenses"><i class="fas fa-receipt me-2"></i>Expenses</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/categories"><i class="fas fa-tags me-2"></i>Categories</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content Area -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <!-- Bootstrap 5 JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 📌 Key Concepts: Template Inheritance

```
layout/base.html          <-- Parent template (defines structure)
    │
    ├── home/dashboard.html    <-- {% extends "layout/base.html" %}
    ├── categories/list.html   <-- {% extends "layout/base.html" %}
    ├── categories/form.html   <-- {% extends "layout/base.html" %}
    ├── expenses/list.html     <-- {% extends "layout/base.html" %}
    ├── expenses/form.html     <-- {% extends "layout/base.html" %}
    └── error.html             <-- {% extends "layout/base.html" %}
```

---

## 📝 Step 2: Create Error Page Template (5 minutes)

Error pages provide user-friendly feedback when something goes wrong.

**Copilot Prompt:**

```text
/generate Create app/templates/error.html extending layout/base.html with:

Centered card layout (col-md-8 col-lg-6)
Error icon (Font Awesome exclamation-triangle, 4x size, text-danger)
"Oops! Something went wrong" heading
Display {{ error }} message or default text
Two buttons:
- "Go to Dashboard" linking to /
- "Go Back" using JavaScript history.back()
Bootstrap styling with shadow card
```

**Expected file**: `app/templates/error.html`

```html
{% extends "layout/base.html" %}

{% block title %}Error - Expense Tracker{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card shadow">
                <div class="card-body text-center py-5">
                    <div class="mb-4">
                        <i class="fas fa-exclamation-triangle fa-4x text-danger"></i>
                    </div>
                    <h2 class="text-danger mb-3">Oops! Something went wrong</h2>
                    <p class="text-muted mb-4">{{ error or 'An unexpected error occurred.' }}</p>
                    <div class="d-flex justify-content-center gap-3">
                        <a href="/" class="btn btn-primary">
                            <i class="fas fa-home me-2"></i>Go to Dashboard
                        </a>
                        <button onclick="history.back()" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left me-2"></i>Go Back
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 📝 Step 3: Create Web Routes with Error Handling (8 minutes)

### 🛤️ Web Routes Setup

**Copilot Prompt:**

```text
/generate Create app/routes/web_routes.py with FastAPI router for web pages:

Setup:
- router = APIRouter(tags=["Web Pages"])
- Jinja2Templates pointing to app/templates directory
- Use os.path.join for cross-platform path handling

Dashboard route (GET /):
- Render home/dashboard.html with metrics
- Wrap in try/except, render error.html on failure

Category routes:
- GET /categories - list all categories, render categories/list.html
- GET /categories/new - render categories/form.html with is_edit=False
- GET /categories/{id}/edit - render categories/form.html with is_edit=True
- POST /categories - handle create, redirect to /categories
- POST /categories/{id}/edit - handle update
- POST /categories/{id}/delete - handle delete

Expense routes:
- GET /expenses - list with optional category_id filter
- GET /expenses/new - form with is_edit=False
- GET /expenses/{id}/edit - form with is_edit=True
- POST /expenses - handle create with notes field
- POST /expenses/{id}/edit - handle update
- POST /expenses/{id}/delete - handle delete

All routes should:
- Use try/except blocks
- Render error.html template on exceptions
- Use status.HTTP_303_SEE_OTHER for redirects after POST
```

**Expected file**: `app/routes/web_routes.py`

```python
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

# Jinja2 templates setup - use os.path for cross-platform compatibility
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))


# ============== Dashboard ==============

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    """Render the main dashboard with key metrics."""
    try:
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


# ============== Categories ==============

@router.get("/categories", response_class=HTMLResponse)
async def list_categories(request: Request, db: AsyncSession = Depends(get_db)):
    """Display all categories with expense counts."""
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
    """Show form to create a new category."""
    return templates.TemplateResponse("categories/form.html", {
        "request": request,
        "is_edit": False  # Flag for form to know it's creating, not editing
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
    """Handle category creation form submission."""
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
    """Show form to edit an existing category."""
    try:
        category = await CategoryService.get_category_by_id(db, category_id)
        return templates.TemplateResponse("categories/form.html", {
            "request": request,
            "category": category,
            "is_edit": True  # Flag for form to know it's editing
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
    """Handle category update form submission."""
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
    """Handle category deletion."""
    try:
        await CategoryService.delete_category(db, category_id)
        return RedirectResponse(url="/categories", status_code=status.HTTP_303_SEE_OTHER)
    except EntityNotFoundException:
        return RedirectResponse(url="/categories", status_code=status.HTTP_303_SEE_OTHER)


# ============== Expenses ==============

@router.get("/expenses", response_class=HTMLResponse)
async def list_expenses(
    request: Request,
    category_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Display all expenses with optional category filtering."""
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
    """Show form to create a new expense."""
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
    notes: Optional[str] = Form(None),  # Optional notes field
    db: AsyncSession = Depends(get_db)
):
    """Handle expense creation form submission."""
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
    """Show form to edit an existing expense."""
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
    """Handle expense update form submission."""
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
    """Handle expense deletion."""
    try:
        await ExpenseService.delete_expense(db, expense_id)
        return RedirectResponse(url="/expenses", status_code=status.HTTP_303_SEE_OTHER)
    except EntityNotFoundException:
        return RedirectResponse(url="/expenses", status_code=status.HTTP_303_SEE_OTHER)
```

### 📌 Key Concept: The `is_edit` Flag Pattern

The `is_edit` flag allows ONE form template to handle BOTH create and edit operations:

```python
# For NEW items (create):
return templates.TemplateResponse("categories/form.html", {
    "request": request,
    "is_edit": False  # Form knows to POST to /categories
})

# For EXISTING items (edit):
return templates.TemplateResponse("categories/form.html", {
    "request": request,
    "category": category,  # Pre-populate form with existing data
    "is_edit": True  # Form knows to POST to /categories/{id}/edit
})
```

In the template:
```html
<!-- Dynamic form action based on is_edit flag -->
<form method="post" action="{{ '/categories/' ~ category.id ~ '/edit' if is_edit else '/categories' }}">
    
    <!-- Dynamic title -->
    <h4>{{ 'Edit' if is_edit else 'New' }} Category</h4>
    
    <!-- Pre-populate fields if editing -->
    <input value="{{ category.name if category else '' }}">
</form>
```

---

## 📝 Step 4: Register Web Routes (2 minutes)

Update `app/main.py` to include the web routes:

**Copilot Prompt:**

```text
Add web_routes import and register with app.include_router() in main.py
```

**Add to `app/main.py`:**

```python
from app.routes.web_routes import router as web_router

# After API router registrations
app.include_router(category_router)
app.include_router(expense_router)
app.include_router(web_router)  # Web pages - add this line
```

---

## ✅ Session 4 Checkpoint

Before proceeding to Session 5, verify:

```bash
# Start application
uvicorn app.main:app --reload --port 8000
```

### Verification Checklist

- [ ] Base template created at `app/templates/layout/base.html`
- [ ] Error template created at `app/templates/error.html`
- [ ] Web routes file created at `app/routes/web_routes.py`
- [ ] Routes registered in `app/main.py`
- [ ] No import errors when starting the server

**Note**: You'll see template errors for missing pages (dashboard, categories, expenses) - that's expected! We'll create those in Session 5.

---

## 🎯 Session 4 Summary

### What You've Built

- **✅ Base Layout Template**: Reusable page structure with responsive navigation
- **✅ Error Page Template**: User-friendly error display
- **✅ Web Routes Infrastructure**: All routes with proper error handling
- **✅ `is_edit` Pattern**: Efficient form reuse pattern

### Key Concepts Learned

1. **Template Inheritance**: Base template with `{% block %}` for child templates
2. **Error Handling**: Try/except blocks rendering error.html
3. **`is_edit` Flag**: Single form template for both create and edit
4. **POST-Redirect-GET**: Using 303 redirects after form submissions

### 📁 Files Created

```
app/
├── templates/
│   ├── layout/
│   │   └── base.html          ✅ Created
│   └── error.html             ✅ Created
└── routes/
    └── web_routes.py          ✅ Created
```

---

## ➡️ Next: Session 5 - Feature Templates

In Session 5, you'll create the actual page templates:
- Dashboard with charts and analytics
- Category list and form templates
- Expense list and form templates (with notes field)

**Continue to**: `5-Day1-Session5-Feature-Templates.md`
