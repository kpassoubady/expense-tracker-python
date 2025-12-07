# 💰 Personal Expense Tracker

A modern, full-stack expense tracking application built with **FastAPI**, **SQLAlchemy**, and **Jinja2**. Track your spending, categorize expenses, and visualize your financial data with an intuitive web interface.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

### Core Functionality
- **📊 Dashboard**: Real-time analytics with spending summaries and charts
- **🏷️ Category Management**: Create, edit, and delete expense categories with custom icons and colors
- **💸 Expense Tracking**: Full CRUD operations for expenses with filtering and search
- **📝 Notes Support**: Add detailed notes to any expense entry
- **📅 Date Filtering**: Filter expenses by category and date range

### Technical Features
- **🚀 Async/Await**: Fully asynchronous API using FastAPI and SQLAlchemy async
- **🔐 Input Validation**: Pydantic schemas for request/response validation
- **🎨 Responsive UI**: Bootstrap 5 with mobile-friendly design
- **📈 Data Visualization**: Chart.js integration for spending analytics
- **🗄️ SQLite Database**: Lightweight, file-based database (easily swappable)
- **📚 API Documentation**: Auto-generated Swagger/OpenAPI docs
- **🧪 Test Coverage**: Comprehensive pytest async test suite

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker-python.git
   cd expense-tracker-python
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Open your browser**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Browser    │  │  REST Client │  │  Swagger/OpenAPI     │   │
│  │  (Jinja2 UI) │  │  (API calls) │  │  (Auto-generated)    │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘   │
└─────────┼─────────────────┼─────────────────────┼───────────────┘
          │                 │                     │
          ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     Routers Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │   │
│  │  │ Web Routes  │  │Category API │  │  Expense API    │   │   │
│  │  │ (HTML/Forms)│  │ (/api/...)  │  │  (/api/...)     │   │   │
│  │  └──────┬──────┘  └──────┬──────┘  └───────┬─────────┘   │   │
│  └─────────┼────────────────┼─────────────────┼─────────────┘   │
│            │                │                 │                 │
│  ┌─────────▼────────────────▼─────────────────▼─────────────┐   │
│  │                    Service Layer                         │   │
│  │  ┌─────────────────────┐  ┌─────────────────────────┐    │   │
│  │  │  CategoryService    │  │    ExpenseService       │    │   │
│  │  │  - CRUD operations  │  │    - CRUD operations    │    │   │
│  │  │  - Business logic   │  │    - Statistics         │    │   │
│  │  └──────────┬──────────┘  └───────────┬─────────────┘    │   │
│  └─────────────┼─────────────────────────┼──────────────────┘   │
│                │                         │                      │
│  ┌─────────────▼─────────────────────────▼──────────────────┐   │
│  │                    Data Layer                            │   │
│  │  ┌─────────────────┐  ┌─────────────────────────────┐    │   │
│  │  │  SQLAlchemy     │  │  Pydantic Schemas           │    │   │
│  │  │  Models         │  │  (Validation/Serialization) │    │   │
│  │  └────────┬────────┘  └─────────────────────────────┘    │   │
│  └───────────┼──────────────────────────────────────────────┘   │
└──────────────┼──────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database Layer                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              SQLite (expense_tracker.db)                 │   │
│  │  ┌─────────────────┐      ┌─────────────────────────┐    │   │
│  │  │   categories    │──1:N─│       expenses          │    │   │
│  │  └─────────────────┘      └─────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Design Patterns Used

- **Repository Pattern**: Services abstract database operations
- **Dependency Injection**: FastAPI's `Depends()` for database sessions
- **DTO Pattern**: Pydantic schemas for data transfer
- **Template Inheritance**: Jinja2 base template with child templates

---

## 📁 Project Structure

```
expense-tracker-python/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Application configuration
│   ├── database.py             # Database connection & session
│   ├── exceptions.py           # Custom exception classes
│   ├── seed_data.py            # Database seeding script
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── category.py         # Category model
│   │   └── expense.py          # Expense model
│   │
│   ├── schemas/                # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── category.py         # Category DTOs
│   │   ├── expense.py          # Expense DTOs
│   │   └── response.py         # API response wrappers
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── category_service.py # Category operations
│   │   └── expense_service.py  # Expense operations
│   │
│   ├── routes/                 # API & web route handlers
│   │   ├── __init__.py
│   │   ├── category_routes.py  # /api/categories endpoints
│   │   ├── expense_routes.py   # /api/expenses endpoints
│   │   └── web_routes.py       # Web page routes
│   │
│   └── templates/              # Jinja2 HTML templates
│       ├── layout/
│       │   └── base.html       # Base template with navigation
│       ├── home/
│       │   └── dashboard.html  # Dashboard with charts
│       ├── categories/
│       │   ├── list.html       # Category listing
│       │   └── form.html       # Create/Edit form
│       ├── expenses/
│       │   ├── list.html       # Expense listing
│       │   └── form.html       # Create/Edit form
│       └── error.html          # Error page
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_services.py        # Service layer tests
│   └── response_check.py       # Response schema tests
│
├── exercises/                  # Training materials
│   └── 2-breakout/             # GitHub Copilot exercises
│
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── README.md                   # This file
├── LICENSE                     # MIT License
└── SECURITY.md                 # Security policy
```

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────┐       ┌─────────────────────────────────┐
│         categories          │       │           expenses              │
├─────────────────────────────┤       ├─────────────────────────────────┤
│ id          INTEGER (PK)    │       │ id            INTEGER (PK)      │
│ name        VARCHAR(100)    │───┐   │ amount        DECIMAL(10,2)     │
│ description VARCHAR(255)    │   │   │ description   VARCHAR(255)      │
│ icon        VARCHAR(50)     │   │   │ expense_date  DATE              │
│ color       VARCHAR(7)      │   └──►│ category_id   INTEGER (FK)      │
│ created_at  DATETIME        │       │ notes         TEXT              │
│ updated_at  DATETIME        │       │ created_at    DATETIME          │
└─────────────────────────────┘       │ updated_at    DATETIME          │
                                      └─────────────────────────────────┘
```

### Table Details

#### `categories`
| Column      | Type         | Constraints          | Description             |
|-------------|--------------|----------------------|-------------------------|
| id          | INTEGER      | PRIMARY KEY, AUTO    | Unique identifier       |
| name        | VARCHAR(100) | NOT NULL, UNIQUE     | Category name           |
| description | VARCHAR(255) | NULL                 | Optional description    |
| icon        | VARCHAR(50)  | DEFAULT 'fas fa-tag' | Font Awesome icon class |
| color       | VARCHAR(7)   | DEFAULT '#6c757d'    | Hex color code        |
| created_at  | DATETIME     | DEFAULT NOW()        | Creation timestamp      |
| updated_at  | DATETIME     | ON UPDATE NOW()      | Last update timestamp   |

#### `expenses`
| Column       | Type          | Constraints        | Description           |
|--------------|---------------|--------------------|-----------------------|
| id           | INTEGER       | PRIMARY KEY, AUTO  | Unique identifier     |
| amount       | DECIMAL(10,2) | NOT NULL, > 0      | Expense amount        |
| description  | VARCHAR(255)  | NOT NULL           | Expense description   |
| expense_date | DATE          | NOT NULL           | Date of expense       |
| category_id  | INTEGER       | FK → categories.id | Associated category   |
| notes        | TEXT          | NULL               | Optional notes        |
| created_at   | DATETIME      | DEFAULT NOW()      | Creation timestamp    |
| updated_at   | DATETIME      | ON UPDATE NOW()    | Last update timestamp |

---

## 🧪 Test Coverage

### Test Categories

| Test File           | Coverage Area        | Tests |
|---------------------|----------------------|-------|
| `test_services.py`  | Service layer logic  | 8+    |
| `response_check.py` | API response schemas | 6+    |
| `conftest.py`       | Shared fixtures      | -     |

### What's Tested

- ✅ Category CRUD operations
- ✅ Expense CRUD operations
- ✅ Duplicate name validation
- ✅ Foreign key constraints
- ✅ API response schema validation
- ✅ Pagination responses
- ✅ Error responses

---

## 🧪 Running Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_services.py -v

# Run tests matching a pattern
pytest tests/ -v -k "category"

# Run with print output visible
pytest tests/ -v -s
```

### Test Configuration

The project uses `pytest.ini` for configuration:

```ini
[pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
```

---

## 📚 API Documentation

### Interactive Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Categories API (`/api/categories`)

| Method | Endpoint               | Description         |
|--------|------------------------|---------------------|
| GET    | `/api/categories`      | List all categories |
| GET    | `/api/categories/{id}` | Get category by ID  |
| POST   | `/api/categories`      | Create new category |
| PUT    | `/api/categories/{id}` | Update category     |
| DELETE | `/api/categories/{id}` | Delete category     |

#### Expenses API (`/api/expenses`)

| Method | Endpoint             | Description        |
|--------|----------------------|--------------------|
| GET    | `/api/expenses`      | List all expenses  |
| GET    | `/api/expenses/{id}` | Get expense by ID  |
| POST   | `/api/expenses`      | Create new expense |
| PUT    | `/api/expenses/{id}` | Update expense     |
| DELETE | `/api/expenses/{id}` | Delete expense     |

#### Web Routes

| Method | Endpoint                  | Description        |
|--------|---------------------------|--------------------|
| GET    | `/`                       | Dashboard          |
| GET    | `/categories`             | Category list      |
| GET    | `/categories/new`         | New category form  |
| GET    | `/categories/{id}/edit`   | Edit category form |
| POST   | `/categories`             | Create category    |
| POST   | `/categories/{id}/edit`   | Update category    |
| POST   | `/categories/{id}/delete` | Delete category    |
| GET    | `/expenses`               | Expense list       |
| GET    | `/expenses/new`           | New expense form   |
| GET    | `/expenses/{id}/edit`     | Edit expense form  |
| POST   | `/expenses`               | Create expense     |
| POST   | `/expenses/{id}/edit`     | Update expense     |
| POST   | `/expenses/{id}/delete`   | Delete expense     |

### Example API Requests

#### Create a Category
```bash
curl -X POST http://localhost:8000/api/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Food",
    "description": "Meals and groceries",
    "icon": "fas fa-utensils",
    "color": "#28a745"
  }'
```

#### Create an Expense
```bash
curl -X POST http://localhost:8000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Lunch at cafe",
    "amount": 25.50,
    "expense_date": "2024-01-15",
    "category_id": 1,
    "notes": "Business meeting lunch"
  }'
```

---

## 🔧 Configuration

### Environment Variables

| Variable     | Default                        | Description         |
|--------------|--------------------------------|---------------------|
| DATABASE_URL | sqlite:///./expense_tracker.db | Database connection |
| APP_TITLE    | Expense Tracker                | Application title   |
| APP_VERSION  | 1.0.0                          | Application version |

### Customization

Edit `app/config.py` to modify default settings:

```python
class Settings(BaseSettings):
    APP_TITLE: str = "Expense Tracker"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./expense_tracker.db"
```

---

## 🚀 Deployment

### Production Considerations

1. **Database**: Switch from SQLite to PostgreSQL/MySQL for production
2. **Security**: Add authentication/authorization
3. **HTTPS**: Use a reverse proxy (nginx) with SSL certificates
4. **Environment**: Use environment variables for sensitive config

### Docker (Coming Soon)

```dockerfile
# Dockerfile example
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔒 Security

For security concerns, please see our [Security Policy](SECURITY.md).

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Chart.js](https://www.chartjs.org/) - JavaScript charting library
- [Font Awesome](https://fontawesome.com/) - Icon library

---

## 📞 Support

If you have any questions or run into issues:

1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the [exercises](exercises/) for detailed guides
3. Open an [Issue](https://github.com/yourusername/expense-tracker-python/issues)

---

**Built with ❤️ using GitHub Copilot**
