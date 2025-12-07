# 🎨 Python Track Setup - Day 1 Frontend

## 🎯 Setup Overview

This guide will help you set up the frontend components for the Personal Expense Tracker web interface using Jinja2 templates and Bootstrap.

**⏱️ Estimated Time**: 10-15 minutes

**Prerequisites**: Complete [day1-backend-setup.md](day1-backend-setup.md) first!

---

## 📋 Prerequisites Check

Before starting, ensure:

- ✅ Backend setup completed
- ✅ `uvicorn app.main:app --reload` runs successfully
- ✅ Health check at `/health` works
- ✅ Virtual environment activated

---

## 📁 Step 1: Verify Frontend Directory Structure

### Check Static and Template Folders

```bash
# Verify directory structure
ls -la app/static/
ls -la app/templates/

# Expected structure:
# app/
# ├── static/
# │   ├── css/
# │   └── js/
# └── templates/
```

### Create Missing Directories (If Needed)

```bash
mkdir -p app/static/{css,js,images}
mkdir -p app/templates/{layout,categories,expenses,home}
```

---

## 🎨 Step 2: Create Base Layout Template

### Create Main Layout

Create `app/templates/layout/base.html`:

**GitHub Copilot Prompt:**

```text
/generate Create Jinja2 base template with:
- HTML5 doctype with responsive meta tags
- Bootstrap 5.3.2 CSS via CDN
- Font Awesome 6.5.0 for icons
- Chart.js 4.4.0 for dashboard charts
- jQuery 3.7.1 for AJAX
- Navigation bar with links: Dashboard, Expenses, Categories
- Flash message display area
- Content block for child templates
- Footer with copyright
- JavaScript block at end of body
```

**Expected file** (`app/templates/layout/base.html`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Personal Expense Tracker{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link href="{{ url_for('static', path='/css/custom.css') }}" rel="stylesheet">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('root') }}">
                <i class="fas fa-wallet me-2"></i>Expense Tracker
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {% if request.url.path == '/' %}active{% endif %}" href="/">
                            <i class="fas fa-tachometer-alt me-1"></i>Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if '/expenses' in request.url.path %}active{% endif %}" href="/expenses">
                            <i class="fas fa-receipt me-1"></i>Expenses
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if '/categories' in request.url.path %}active{% endif %}" href="/categories">
                            <i class="fas fa-tags me-1"></i>Categories
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Flash Messages -->
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <!-- Main Content -->
    <main class="container mt-4 mb-5">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-light py-3 mt-auto">
        <div class="container text-center text-muted">
            <small>&copy; 2024 Personal Expense Tracker | Built with FastAPI + Copilot</small>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="{{ url_for('static', path='/js/app.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## 🎨 Step 3: Create Custom CSS

### Create Custom Styles

Create `app/static/css/custom.css`:

**GitHub Copilot Prompt:**

```text
/generate Create CSS file with:
- Color scheme: primary #4A90E2, success #7ED321, danger #D0021B
- Dashboard card styling with shadows and hover effects
- Responsive table styling
- Form styling improvements
- Chart container sizing
- Category badge colors
- Button animations
- Mobile-responsive adjustments
```

**Expected file** (`app/static/css/custom.css`):

```css
/* Custom Color Scheme */
:root {
    --primary-color: #4A90E2;
    --success-color: #7ED321;
    --danger-color: #D0021B;
    --warning-color: #F5A623;
    --info-color: #50E3C2;
}

/* Dashboard Cards */
.dashboard-card {
    border: none;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.dashboard-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.dashboard-card .card-body {
    padding: 1.5rem;
}

.dashboard-card .icon-circle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

/* Category Colors */
.category-badge {
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
}

/* Responsive Tables */
@media (max-width: 768px) {
    .table-responsive-stack tr {
        display: block;
        border-bottom: 2px solid #dee2e6;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
    }
    
    .table-responsive-stack td {
        display: flex;
        justify-content: space-between;
        border: none;
        padding: 0.5rem 0;
    }
    
    .table-responsive-stack td::before {
        content: attr(data-label);
        font-weight: bold;
        margin-right: 1rem;
    }
}

/* Form Styling */
.form-control:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(74, 144, 226, 0.25);
}

.form-label {
    font-weight: 500;
    color: #495057;
}

/* Button Animations */
.btn {
    transition: all 0.2s ease;
}

.btn:hover {
    transform: translateY(-1px);
}

.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.btn-primary:hover {
    background-color: #3a7bc8;
    border-color: #3a7bc8;
}

/* Chart Container */
.chart-container {
    position: relative;
    height: 300px;
    width: 100%;
}

@media (max-width: 576px) {
    .chart-container {
        height: 250px;
    }
}

/* Amount Display */
.amount-positive {
    color: var(--success-color);
    font-weight: 600;
}

.amount-negative {
    color: var(--danger-color);
    font-weight: 600;
}

/* Loading Spinner */
.loading-spinner {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 3rem;
    color: #6c757d;
}

.empty-state i {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}
```

---

## 📜 Step 4: Create Base JavaScript

### Create App JavaScript

Create `app/static/js/app.js`:

**GitHub Copilot Prompt:**

```text
/generate Create JavaScript file with:
- Document ready handler
- AJAX error handling utility
- Delete confirmation dialogs
- Chart initialization helpers
- Form validation helpers
- Flash message auto-dismiss (5 seconds)
- API call utility functions
```

**Expected file** (`app/static/js/app.js`):

```javascript
// Personal Expense Tracker - Main JavaScript

$(document).ready(function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// API Utility Functions
const api = {
    baseUrl: '/api',
    
    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    },
    
    async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    },
    
    async delete(endpoint) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API DELETE Error:', error);
            throw error;
        }
    }
};

// Delete Confirmation
function confirmDelete(itemName, deleteUrl) {
    if (confirm(`Are you sure you want to delete "${itemName}"? This action cannot be undone.`)) {
        window.location.href = deleteUrl;
    }
}

// Chart Initialization Helper
function initPieChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    return new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || [
                    '#FF6B6B', '#4ECDC4', '#45B7D1', 
                    '#96CEB4', '#FECA57', '#FF9FF3'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function initLineChart(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label || 'Amount',
                data: data,
                borderColor: '#4A90E2',
                backgroundColor: 'rgba(74, 144, 226, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Currency Formatting
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Date Formatting
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Loading State Helper
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading-spinner"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
    }
}

function hideLoading(elementId, content) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = content;
    }
}

console.log('✅ Expense Tracker JS loaded');
```

---

## ✅ Step 5: Verify Frontend Setup

### Test Static Files

```bash
# Start the application
uvicorn app.main:app --reload

# Test static file serving
curl http://localhost:8000/static/css/custom.css
curl http://localhost:8000/static/js/app.js
```

### Check Browser Console

1. Open http://localhost:8000 in browser
2. Open Developer Tools (F12)
3. Check Console tab for "✅ Expense Tracker JS loaded" message
4. Check Network tab - all static files should load (200 status)

---

## ✅ Frontend Setup Checklist

Before starting Session 4, verify:

- [ ] `app/templates/layout/base.html` exists
- [ ] `app/static/css/custom.css` exists
- [ ] `app/static/js/app.js` exists
- [ ] Static files load in browser
- [ ] No JavaScript errors in console
- [ ] Bootstrap styling visible
- [ ] Font Awesome icons work

---

## 🎯 Next Steps

**Frontend setup complete!**

You're now ready for:
- **Session 4**: [Web Interface & Templates](../2-breakout/4-Day1-Session4-Web-Interface-Templates.md)

In Session 4, you'll:
- Create dashboard with charts and analytics
- Build category and expense management pages
- Add AJAX interactivity
- Practice multi-language Copilot coordination

**Happy coding! 🚀**
