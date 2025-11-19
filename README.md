# 💰 Save My Wallet - Backend API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.3-336791?logo=postgresql&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-99%25-brightgreen)
![Tests](https://img.shields.io/badge/Tests-478_passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

*Backend API for personal finance management built with FastAPI and Clean Architecture*

[Documentation](#-api-documentation) • [Installation](#-installation) • [Architecture](#-architecture) • [Testing](#-testing)

</div>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Testing](#-testing)
- [API Documentation](#-api-documentation)
- [License](#-license)

---

## 🎯 About the Project

**Save My Wallet** is a robust backend application for personal finance management that allows users to:

- 💳 Manage credit cards
- 📊 Track expenses (purchases and subscriptions)
- 🏷️ Categorize expenses
- 💵 Record payments
- 📈 Query financial history with pagination

The project is designed following **Clean Architecture** principles, ensuring maintainable, testable, and scalable code.

---

## ✨ Key Features

### 🔐 Authentication and Authorization
- Registration and login system with JWT
- Automatic token renewal
- Role and permission management

### 💳 Credit Card Management
- Complete CRUD operations for cards
- Credit limit tracking
- Closing and payment due dates

### 📊 Expense Tracking
- **Purchases:** One-time expenses with multiple installments
- **Subscriptions:** Recurring monthly expenses
- Custom categorization
- Payment status (pending, paid, overdue)

### 💰 Payment System
- Payment recording per installment
- Automatic expense status updates
- Payment history

### � Period Management
- **Current Period:** View all payments for the current billing period
- **Period History:** Query any specific period by month/year
- **Period Projection:** 12-month forecast with subscription simulation
- **Enriched Data:** Each payment includes full expense and account details
- **Subscription Simulation:** Automatic future payment generation for active subscriptions

### �📈 Queries and Reports
- Efficient result pagination
- Filters by date, category, status
- Search and sorting

---

## 🏗️ Architecture

The project implements **Clean Architecture** (Hexagonal Architecture) with clear layer separation:

```mermaid
graph TB
    subgraph "Presentation Layer"
        API[FastAPI Entrypoints]
        Controllers[Controllers]
        Routes[Routes]
        Middleware[Middlewares]
    end
    
    subgraph "Application Layer"
        UseCases[Use Cases]
        DTOs[DTOs]
        Ports[Ports/Interfaces]
    end
    
    subgraph "Domain Layer"
        Entities[Entities]
        ValueObjects[Value Objects]
        Factories[Factories]
        DomainExceptions[Domain Exceptions]
    end
    
    subgraph "Infrastructure Layer"
        Repositories[SQL Repositories]
        Database[Database Models]
        External[External Services]
    end
    
    API --> Controllers
    Controllers --> UseCases
    UseCases --> Entities
    UseCases --> Ports
    Repositories -.implements.-> Ports
    Repositories --> Database
    Entities --> ValueObjects
    Factories --> Entities
    
    style API fill:#e1f5ff
    style Controllers fill:#e1f5ff
    style UseCases fill:#fff4e1
    style DTOs fill:#fff4e1
    style Entities fill:#e8f5e9
    style ValueObjects fill:#e8f5e9
    style Repositories fill:#fce4ec
    style Database fill:#fce4ec
```

### Data Flow

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant UseCase
    participant Entity
    participant Repository
    participant Database

    Client->>Controller: HTTP Request
    Controller->>Controller: Validate & Parse DTO
    Controller->>UseCase: Execute(DTO)
    UseCase->>Repository: Get/Save Entity
    Repository->>Database: SQL Query
    Database-->>Repository: Result
    Repository-->>UseCase: Domain Entity
    UseCase->>Entity: Business Logic
    Entity-->>UseCase: Updated Entity
    UseCase-->>Controller: Result DTO
    Controller-->>Client: HTTP Response
```

### Architecture Layers

| Layer | Responsibility | Key Components |
|------|----------------|-------------------|
| **Domain** | Pure business logic | Entities, Value Objects, Factories, Domain Exceptions |
| **Application** | Use cases and orchestration | Use Cases, DTOs, Ports (interfaces) |
| **Infrastructure** | Technical implementation | SQL Repositories, DB Models, External Services |
| **Presentation** | REST API | Controllers, Routes, Middlewares, Validation |

---

## 🛠 Tech Stack

### Core Framework
| Technology | Version | Purpose |
|-----------|---------|-----------|
| **Python** | 3.14.0 | Programming language |
| **FastAPI** | 0.121.1 | Async web framework |
| **Uvicorn** | 0.38.0 | ASGI server |
| **Pydantic** | 2.12.4 | Data validation and settings |

### Database
| Technology | Version | Purpose |
|-----------|---------|-----------|
| **PostgreSQL** | 16.3 | Relational database |
| **SQLAlchemy** | 2.0.44 | ORM |
| **Alembic** | 1.17.1 | Database migrations |
| **psycopg2** | 2.9.11 | PostgreSQL driver |

### Security
| Technology | Version | Purpose |
|-----------|---------|-----------|
| **PyJWT** | 2.10.1 | JWT authentication |
| **bcrypt** | 5.0.0 | Password hashing |

### Testing & Quality
| Technology | Version | Purpose |
|-----------|---------|-----------|
| **pytest** | 9.0.1 | Testing framework |
| **coverage** | 7.7.0 | Code coverage |

### Containerization
| Technology | Purpose |
|-----------|-----------|
| **Docker** | Application containerization |
| **Docker Compose** | Container orchestration |

---

## 📁 Project Structure

---

## 📁 Estructura del Proyecto

```
smw-back/
│
├── src/                                    # Source code
│   │
│   ├── domain/                            # 🎯 Domain Layer (Business Logic)
│   │   ├── account/                       # Account and Card Aggregate
│   │   │   ├── account.py                 # Account Entity
│   │   │   ├── credit_card.py            # Credit Card Entity
│   │   │   └── credit_card_factory.py    # Credit Card Factory
│   │   ├── auth/                          # Authentication Aggregate
│   │   │   ├── user.py                    # User Entity
│   │   │   ├── profile.py                 # Profile Entity
│   │   │   ├── preferences.py             # Preferences Entity
│   │   │   ├── user_factory.py            # User Factory
│   │   │   └── enums/role.py              # Role Enum
│   │   ├── expense/                       # Expense Aggregate
│   │   │   ├── expense.py                 # Base Expense Entity
│   │   │   ├── purchase.py                # Purchase Entity
│   │   │   ├── subscription.py            # Subscription Entity
│   │   │   ├── payment.py                 # Payment Entity
│   │   │   ├── period.py                  # Period Entity
│   │   │   ├── period_payment.py          # PeriodPayment Value Object
│   │   │   ├── expense_category.py        # Category Entity
│   │   │   ├── *_factory.py               # Factories
│   │   │   ├── enums/                     # Enumerations
│   │   │   └── exceptions/                # Domain exceptions
│   │   └── shared/                        # Shared components
│   │       ├── entity_base.py             # Base class for entities
│   │       ├── entity_factory_base.py     # Base class for factories
│   │       ├── exception_base.py          # Base class for exceptions
│   │       ├── value_objects/             # Value Objects (Amount, Year, Month)
│   │       └── helpers/dates.py           # Date helpers
│   │
│   ├── application/                       # 💼 Application Layer (Use Cases)
│   │   ├── use_cases/                     # Use cases
│   │   │   ├── auth/                      # Authentication use cases
│   │   │   │   ├── user_login_use_case.py
│   │   │   │   ├── user_register_use_case.py
│   │   │   │   └── user_renew_token_use_case.py
│   │   │   ├── account/                   # Account use cases
│   │   │   │   ├── credit_card_create_use_case.py
│   │   │   │   ├── credit_card_get_*.py
│   │   │   │   └── credit_card_update/delete_use_case.py
│   │   │   ├── expense/                   # Expense use cases
│   │   │   │   ├── purchase_*.py
│   │   │   │   ├── subscription_*.py
│   │   │   │   ├── payment_*.py
│   │   │   │   └── expense_category_*.py
│   │   │   └── user/                      # User use cases
│   │   │   ├── dtos/                          # Data Transfer Objects
│   │   │   ├── auth_dtos.py
│   │   │   ├── credit_card_dtos.py
│   │   │   ├── expense_dtos.py
│   │   │   ├── payment_dtos.py
│   │   │   ├── period_dtos.py             # Period DTOs
│   │   │   ├── user_dtos.py
│   │   │   └── pagination_dtos.py
│   │   ├── ports/                         # Interfaces (repository contracts)
│   │   │   ├── base_repository.py
│   │   │   ├── credit_card_repository.py
│   │   │   ├── expense_repository.py
│   │   │   └── user_repository.py
│   │   ├── helpers/                       # Application helpers
│   │   │   └── security.py                # Security helpers (JWT, bcrypt)
│   │   └── exceptions/                    # Application exceptions
│   │
│   ├── infrastructure/                    # 🔧 Infrastructure Layer
│   │   ├── database/                      # Database configuration
│   │   │   ├── database_connection.py     # SQLAlchemy configuration
│   │   │   └── models/                    # ORM models (SQLAlchemy)
│   │   │       ├── base_model.py
│   │   │       ├── user_model.py
│   │   │       ├── account_model.py
│   │   │       ├── credit_card_model.py
│   │   │       ├── expense_model.py
│   │   │       └── payment_model.py
│   │   └── repositories/                  # Repository implementations
│   │       ├── base_repository_sql.py     # Base repository with CRUD operations
│   │       ├── user_repository_sql.py
│   │       ├── credit_card_repository_sql.py
│   │       ├── expense_repository_sql.py
│   │       └── payment_repository_sql.py
│   │
│   ├── entrypoints/                       # 🌐 Presentation Layer (API)
│   │   ├── api.py                         # FastAPI app configuration
│   │   ├── controllers/                   # HTTP controllers
│   │   │   ├── auth_controller.py
│   │   │   ├── account_controller.py
│   │   │   ├── expense_controller.py
│   │   │   ├── period_controller.py       # Period controller
│   │   │   └── user_controller.py
│   │   ├── routes/                        # Route definitions
│   │   │   ├── v1/
│   │   │   ├── v2/
│   │   │   └── v3/                        # Period routes
│   │   ├── dependencies/                  # FastAPI dependency injection
│   │   │   └── auth_dependencies.py       # Authentication dependencies
│   │   ├── middlewares/                   # HTTP middlewares
│   │   │   └── jwt_middleware.py
│   │   └── exceptions/                    # HTTP exception handlers
│   │       ├── base_http_exception.py
│   │       ├── client_exceptions.py       # 4xx errors
│   │       └── server_exceptions.py       # 5xx errors
│   │
│   ├── common/                            # 📦 Shared code
│   │   ├── error_codes.py                 # Error codes
│   │   └── exceptions/                    # Common exceptions
│   │
│   └── config.py                          # ⚙️ Global configuration (Settings)
│
├── tests/                                 # 🧪 Test suite (478 tests)
│   ├── domain/                            # Domain tests
│   ├── application/                       # Use case tests
│   ├── infrastructure/                    # Repository tests
│   └── entrypoints/                       # API tests
│
├── migrations/                            # 📝 Alembic migrations
│   ├── versions/
│   └── env.py
│
├── logs/                                  # 📋 Log files
│
├── docker-compose.yml                     # 🐳 Docker Compose configuration
├── Dockerfile                             # 🐳 Docker image
├── requirements.txt                       # 📦 Python dependencies
├── alembic.ini                           # ⚙️ Alembic configuration
├── __main__.py                           # 🚀 Application entry point
├── run-dev.sh                            # 🔧 Development script
├── run.sh                                # 🚀 Production script
└── build.sh                              # 🏗️ Build script
```

---

## 🚀 Installation

### Prerequisites

| Requirement | Minimum Version | Check |
|-----------|----------------|-----------|
| Python | 3.10+ | `python --version` |
| PostgreSQL | 12+ | `psql --version` |
| Docker *(optional)* | 20+ | `docker --version` |
| Docker Compose *(optional)* | 2.0+ | `docker-compose --version` |

---

### 🐍 Local Installation (Development)

#### 1. Clone the Repository

```bash
git clone https://github.com/tu-usuario/smw-back.git
cd smw-back
```

#### 2. Create Virtual Environment

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (includes testing)
pip install -r requirements-dev.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database
CONN_DB=postgresql://username:password@localhost:5432/save_my_wallet

# JWT
JWT_SECRET_KEY=your-super-secure-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Application
ENVIRONMENT=development
DEBUG=True
```

#### 5. Setup Database

```bash
# Create PostgreSQL database
createdb save_my_wallet

# Run migrations
alembic upgrade head
```

#### 6. Run Development Server

```bash
# Using script
./run-dev.sh

# Or manually
uvicorn src.entrypoints.api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

---

### 🐳 Docker Installation (Production)

#### 1. Configure Environment Variables

Create a `.env` file:

```env
CONN_DB=postgresql://postgres:postgres@smw-db:5432/save_my_wallet
JWT_SECRET_KEY=your-super-secure-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
REFRESH_TOKEN_EXPIRATION_DAYS=30
ENVIRONMENT=production
DEBUG=False
```

#### 2. Setup Docker Compose Override (Optional)

For local development or testing, create a `docker-compose.override.yml` file to expose ports:

```bash
# Copy the example override file
cp docker-compose.eg-override.yml docker-compose.override.yml
```

The override file allows you to customize your local environment without modifying the base configuration:

```yaml
services:
    smw-api:
        ports:
            - "8000:8000"  # Expose API port for local access
    
    smw-db:
        environment:
            POSTGRES_PASSWORD: "root"
            POSTGRES_USER: "root"
        ports:
            - "5432:5432"  # Expose DB port for local access
```

**Note:** The `docker-compose.override.yml` file is git-ignored, allowing each developer to have their own configuration.

#### 3. Build and Run Containers

```bash
# Build images
docker-compose build

# Start services (uses docker-compose.override.yml automatically if it exists)
docker-compose up -d

# View logs
docker-compose logs -f smw-api
```

#### 4. Run Migrations

```bash
docker-compose exec smw-api alembic upgrade head
```

#### 5. Verify Status

```bash
# View running containers
docker-compose ps

# Test API (only if you have the override file with exposed ports)
curl http://localhost:8000/docs
```

**Note:** Without a `docker-compose.override.yml` file, the API will run but won't be accessible from the host machine. This is useful for production deployments where you might use a reverse proxy or internal networking.

---

### 🔄 Environment Differences

| Aspect | Development | Production |
|---------|------------|------------|
| **Server** | Uvicorn (reload) | Gunicorn + Uvicorn workers |
| **Debug** | Enabled | Disabled |
| **Hot Reload** | ✅ Yes | ❌ No |
| **Logs** | Console + file | Rotating file |
| **Database** | Local PostgreSQL | PostgreSQL in container |
| **Workers** | 1 | Multiple (based on CPU) |
| **.env Variables** | Loaded from file | Loaded from Docker |

---

## 🎮 Usage

### 📖 API Documentation

Once the server is running, access the interactive documentation:

| Type | URL | Description |
|------|-----|-------------|
| **Swagger UI** | http://localhost:8000/docs | Interactive documentation with testing |
| **ReDoc** | http://localhost:8000/redoc | Clean and readable documentation |
| **OpenAPI JSON** | http://localhost:8000/openapi.json | OpenAPI 3.0 specification |

---

### 🔐 Authentication

The API uses **JWT (JSON Web Tokens)** for authentication:

#### 1. User Registration

```bash
curl -X POST "http://localhost:8000/api/v2/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v2/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### 3. Use Token in Requests

Include the token in the `Authorization` header:

```bash
curl -X GET "http://localhost:8000/api/v2/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 📌 Main Endpoints

#### Authentication (`/api/v2/auth`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Register user | ❌ |
| POST | `/login` | Login | ❌ |
| GET | `/renew` | Renew JWT token | ✅ |

#### Users (`/api/v2/users`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/me` | Get current profile | ✅ |
| PUT | `/me` | Update profile | ✅ |

#### Credit Cards (`/api/v2/credit-cards`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List cards (paginated) | ✅ |
| POST | `/` | Create card | ✅ |
| GET | `/{id}` | Get card details | ✅ |
| PUT | `/{id}` | Update card | ✅ |
| DELETE | `/{id}` | Delete card | ✅ |

#### Expense Categories (`/api/v2/expense-categories`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List categories (paginated) | ✅ |
| POST | `/` | Create category | ✅ |
| PUT | `/{id}` | Update category | ✅ |
| DELETE | `/{id}` | Delete category | ✅ |

#### Expenses (`/api/v2/expenses`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List all expenses (paginated) | ✅ |
| POST | `/purchases` | Create purchase | ✅ |
| GET | `/purchases/{id}` | Get purchase | ✅ |
| PUT | `/purchases/{id}` | Update purchase | ✅ |
| DELETE | `/purchases/{id}` | Delete purchase | ✅ |
| POST | `/subscriptions` | Create subscription | ✅ |
| GET | `/subscriptions/{id}` | Get subscription | ✅ |
| PUT | `/subscriptions/{id}` | Update subscription | ✅ |
| DELETE | `/subscriptions/{id}` | Delete subscription | ✅ |

#### Payments (`/api/v2/payments`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/` | Register installment payment | ✅ |
| PUT | `/{id}` | Update payment | ✅ |
| DELETE | `/{id}` | Delete payment | ✅ |

#### Periods (`/api/v3/periods`) 🆕

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/current` | Get current billing period | ✅ |
| GET | `/{month}/{year}` | Get specific period | ✅ |
| GET | `/projection` | Get 12-month projection | ✅ |

**Period Response includes:**
- All payments with enriched data (expense details + account info)
- Calculated totals (total, confirmed, paid, pending)
- Payment counters (total, pending, completed)
- Automatic subscription simulation for future periods

---

### 💡 Usage Examples

#### Create a Credit Card

```bash
curl -X POST "http://localhost:8000/api/v2/credit-cards" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Visa Gold",
    "last_four_digits": "1234",
    "credit_limit": 50000,
    "closing_day": 15,
    "payment_due_day": 5
  }'
```

#### Create a Purchase

```bash
curl -X POST "http://localhost:8000/api/v2/expenses/purchases" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Dell Laptop",
    "total_amount": 120000,
    "installments": 12,
    "purchase_date": "2025-01-15",
    "credit_card_id": "card-uuid",
    "category_id": "category-uuid"
  }'
```

#### Register a Payment

```bash
curl -X POST "http://localhost:8000/api/v2/payments" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "expense_id": "expense-uuid",
    "installment_number": 1,
    "paid_amount": 10000,
    "payment_date": "2025-02-05"
  }'
```

#### Get Current Period

```bash
curl -X GET "http://localhost:8000/api/v3/periods/current" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "id": "period-uuid",
  "period_str": "11/2025",
  "month": 11,
  "year": 2025,
  "total_amount": 45000.00,
  "total_confirmed_amount": 35000.00,
  "total_paid_amount": 20000.00,
  "total_pending_amount": 10000.00,
  "total_payments": 8,
  "pending_payments_count": 3,
  "completed_payments_count": 5,
  "payments": [
    {
      "payment_id": "uuid",
      "amount": 5000.00,
      "status": "confirmed",
      "payment_date": "2025-11-15",
      "no_installment": 3,
      "is_last_payment": false,
      "expense_id": "uuid",
      "expense_title": "Dell Laptop",
      "expense_cc_name": "DELL-LAPTOP",
      "expense_acquired_at": "2025-09-01",
      "expense_installments": 12,
      "expense_status": "active",
      "expense_category_name": "Electronics",
      "account_id": "uuid",
      "account_alias": "Visa Gold",
      "account_is_enabled": true,
      "account_type": "credit_card"
    }
  ]
}
```

#### Get 12-Month Projection

```bash
curl -X GET "http://localhost:8000/api/v3/periods/projection" \
  -H "Authorization: Bearer $TOKEN"
```

Returns an array of 12 periods including simulated payments for active subscriptions.

---

## 🧪 Testing

The project has **99% code coverage** and **478 tests** that verify:

- ✅ Domain logic (entities, value objects, factories)
- ✅ Use cases (application layer)
- ✅ Repositories (infrastructure layer)
- ✅ Controllers and endpoints (presentation layer)
- ✅ Validations and error handling

### 📊 Current Coverage

```
Coverage: 99%
Total Statements: 2,492
Missing Lines: 25
Tests: 478 passing
```

### Run Tests

```bash
# All tests
pytest

# With detailed report
pytest -v

# Specific tests
pytest tests/domain/
pytest tests/application/use_cases/

# With coverage
python -m coverage run -m pytest tests/
python -m coverage report --omit="tests/*"

# Generate HTML report
python -m coverage html
# Open htmlcov/index.html in browser
```

### Test Structure

```
tests/
├── domain/                    # Domain entities and business logic tests
│   ├── test_credit_card.py
│   ├── test_expense.py
│   ├── test_user.py
│   └── test_value_objects.py
├── application/               # Use case tests
│   ├── use_cases/
│   │   ├── test_auth_use_cases.py
│   │   ├── test_credit_card_use_cases.py
│   │   └── test_expense_use_cases.py
│   └── dtos/
│       └── test_dtos.py
├── infrastructure/            # Repository tests
│   └── repositories/
│       ├── test_base_repository.py
│       └── test_credit_card_repository.py
└── entrypoints/              # API tests
    └── controllers/
        ├── test_auth_controller.py
        └── test_expense_controller.py
```

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Save My Wallet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📧 Contact and Contributions

### 🤝 Contributing to the Project

Contributions are welcome! To contribute:

1. **Fork** the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add: new feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**

### 📋 Contribution Guidelines

- Follow Clean Architecture principles
- Write tests for new features
- Maintain code coverage > 95%
- Document functions and classes with docstrings
- Use type hints in Python
- Follow PEP 8 for code style

### 🐛 Report Issues

If you find a bug or have a suggestion:

1. Check [existing issues](https://github.com/juanpanasiti/smw-back/issues)
2. If it doesn't exist, create a new issue with:
   - Clear description of the problem/suggestion
   - Steps to reproduce (if it's a bug)
   - Environment (OS, Python version, etc.)

---

<div align="center">

**⭐ If you like this project, give it a star on GitHub ⭐**

[Documentation](https://github.com/juanpanasiti/smw-back) • [Report Bug](https://github.com/juanpanasiti/smw-back/issues) • [Request Feature](https://github.com/juanpanasiti/smw-back/issues)

---

Made with ❤️ using FastAPI and Clean Architecture

</div>
