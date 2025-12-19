# 🛒 Comercio - E-Commerce Platform

A modern, full-stack e-commerce web application built with **FastAPI** (backend) and **vanilla JavaScript** (frontend). Features user authentication, product management, shopping cart, and secure checkout with real-time inventory management.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121-green)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)
![Tests](https://img.shields.io/badge/Tests-41%20passing-success)

---

## ✨ Features

### 🔐 User Authentication
- Secure registration with password hashing (Argon2)
- Session-based authentication with HTTP-only cookies
- Profile management (view/update user information)
- Logout functionality

### 🛍️ Product Management
- Browse products grouped by category
- Real-time stock availability display
- Product search functionality
- Low stock warnings

### 🛒 Shopping Cart
- Add/remove items from cart
- Persistent cart (localStorage)
- Quantity validation against stock
- Real-time total calculation

### 💳 Checkout Process
- Secure order processing
- Inventory reduction at checkout (not when adding to cart)
- Stock validation during checkout
- Atomic transactions (rollback on failure)
- Order history tracking

### 🧪 Testing
- **41 comprehensive tests** across all backend modules
- **100% pass rate** for authentication, products, and orders
- Isolated test database
- Fixtures for rapid testing

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **Passlib + Argon2** - Password hashing
- **Pydantic** - Data validation

### Frontend
- **Vanilla JavaScript** - No framework overhead
- **Bootstrap 5** - Responsive UI components
- **Font Awesome** - Icons
- **HTML5/CSS3** - Modern web standards

### Testing
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **httpx** - HTTP client for testing
- **TestClient** - FastAPI testing utilities

---

## 📁 Project Structure

```
comercio/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration
├── auth.py                 # Session management
├── requirements.txt        # Python dependencies
├── seed_product.py         # Database seeding script
│
├── models/                 # SQLAlchemy models
│   ├── users.py           # User model
│   ├── products.py        # Product model
│   └── order.py           # Order models
│
├── routers/               # API route handlers
│   ├── users.py          # User endpoints
│   ├── products.py       # Product endpoints
│   └── order.py          # Order/checkout endpoints
│
├── controller/           # Business logic
│   └── user.py          # Password hashing utilities
│
├── views/               # Frontend files
│   ├── Web.html        # Main page
│   ├── RegistrationForm.html
│   ├── FQA.html
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript libraries
│   ├── style/         # Custom styles & scripts
│   ├── images/        # Product images
│   └── webfonts/      # Font files
│
└── tests/             # Test suite
    ├── conftest.py           # Test fixtures
    ├── test_auth.py          # Auth tests
    ├── test_database.py      # Database tests
    ├── test_main.py          # App tests
    ├── test_users.py         # User endpoint tests
    ├── test_products.py      # Product endpoint tests
    └── test_order.py         # Order endpoint tests
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **pip** (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd comercio
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize database**
   ```bash
   python seed_product.py
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

7. **Open in browser**
   ```
   http://127.0.0.1:8000
   ```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Module
```bash
pytest tests/test_users.py -v
pytest tests/test_order.py -v
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html
```

### Test Results
- **Total Tests**: 41
- **Pass Rate**: 100%
- **Coverage**: Authentication, Database, Users, Products, Orders

---

## 📡 API Endpoints

### Authentication & Users
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/register-user` | Register new user | ❌ |
| `POST` | `/login` | User login | ❌ |
| `GET` | `/me` | Get current user | ✅ |
| `PUT` | `/update-profile` | Update user profile | ✅ |
| `POST` | `/logout` | Logout user | ✅ |

### Products
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/products/grouped` | Get products by category | ❌ |
| `GET` | `/products/search?q={query}` | Search products | ❌ |

### Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/order/checkout` | Process checkout | ✅ |

---

## 🔑 Key Features Explained

### Inventory Management
- **Add to Cart**: Stock is NOT reduced from database
- **Checkout**: Stock is validated and reduced atomically
- **Benefits**:
  - Prevents stock reservation for abandoned carts
  - Accurate real-time inventory
  - Handles concurrent checkouts safely

### Security
- **Password Hashing**: Argon2 algorithm
- **Session Tokens**: URL-safe, randomly generated
- **HTTP-Only Cookies**: Prevents XSS attacks
- **Server-Side Validation**: All inputs validated

### Database
- **SQLite**: Lightweight, file-based database
- **SQLAlchemy ORM**: Type-safe database queries
- **Migrations**: Manual schema management
- **Test Database**: Separate `test_db.sqlite3` for testing

---

## 📝 Environment Variables

No environment variables required for local development. The application uses:
- SQLite database: `db.sqlite3`
- Test database: `test_db.sqlite3`
- Default port: `8000`

---

## 🔧 Development

### Code Structure Guidelines
- **Models**: SQLAlchemy models in `models/`
- **Routes**: API endpoints in `routers/`
- **Business Logic**: Helper functions in `controller/`
- **Frontend**: Static files in `views/`

### Adding New Features
1. Create/update model in `models/`
2. Add route handler in `routers/`
3. Write tests in `tests/`
4. Update frontend in `views/`

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📊 Database Schema

### Users
- `id` (Primary Key)
- `email` (Unique)
- `password` (Hashed)
- `first_name`, `last_name`
- `phone`, `country`, `dob`, `sex`

### Products
- `id` (Primary Key)
- `name`, `description`
- `price`, `image_url`
- `category`, `stock_avilabilty`

### Orders
- **OrderDetails**: `id`, `user_id`, `total_price`
- **OrderItems**: `id`, `order_details_id`, `product_id`, `product_name`, `price`, `quantity`

---

## 🚨 Common Issues

### Database Locked
```bash
# Delete database and re-seed
rm db.sqlite3
python seed_product.py
```

### Port Already in Use
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

### Module Not Found
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```


