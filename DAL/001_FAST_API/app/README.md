# VishAgent - Data Access Layer (DAL) Details

## What is the Data Access Layer (DAL)?

The **Data Access Layer (DAL)** is a software architecture pattern that abstracts and encapsulates database operations. It sits between the business logic layer (services) and the actual database, providing a uniform interface for data operations.

### Architecture Layer Positioning

```
┌─────────────────────────────────────┐
│    API Layer (Routes/Endpoints)     │
├─────────────────────────────────────┤
│      Services (Business Logic)      │
├─────────────────────────────────────┤
│    DAL (Data Access Layer) ← YOU ARE HERE
├─────────────────────────────────────┤
│   Database (PostgreSQL, MongoDB)    │
└─────────────────────────────────────┘
```

### Key Responsibility

The DAL is responsible for:
- Reading data from databases
- Writing data to databases
- Updating records
- Deleting records
- Querying and filtering data
- Transaction management
- Connection pooling
- Query optimization

---

## Why is DAL Important?

### 1. **Separation of Concerns**
Decouples business logic from database implementation details.

```python
# ❌ WITHOUT DAL (Bad Practice)
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Business logic mixed with database code
    connection = psycopg2.connect("dbname=test")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    connection.close()
    return user  # Hard to test, hard to change database

# ✅ WITH DAL (Good Practice)
user_dal = UserDAL()
user = await user_dal.get_user_by_id(user_id)  # Clean, testable
```

### 2. **Testability**
Easy to mock database operations without hitting a real database.

```python
# Mock the DAL for testing
class MockUserDAL:
    async def get_user_by_id(self, user_id: int):
        return User(id=1, name="Test User")

# Test business logic without database
def test_user_service():
    service = UserService(dal=MockUserDAL())
    user = service.get_user(1)
    assert user.name == "Test User"
```

### 3. **Maintainability**
Change database implementation without touching service/endpoint code.

```python
# Change from PostgreSQL to MongoDB - only update DAL
# All services continue working unchanged

class UserDAL:
    async def get_user_by_id(self, user_id: int) -> User:
        # PostgreSQL: SELECT * FROM users WHERE id = $1
        # MongoDB: db.users.find_one({"_id": user_id})
        # Implementation changes, interface stays the same
        pass
```

### 4. **Code Reusability**
Same database operation used across multiple services.

```python
# UserDAL methods used by multiple services
class UserDAL:
    async def get_user_by_id(self, user_id: int) -> User: pass
    async def create_user(self, user: User) -> User: pass
    async def update_user(self, user: User) -> User: pass
    async def delete_user(self, user_id: int) -> bool: pass

# Used by UserService, AuthService, NotificationService
```

### 5. **Query Optimization**
Centralized location for database optimization and caching.

```python
class UserDAL:
    def __init__(self):
        self.cache = {}  # Simple caching
    
    async def get_user_by_id(self, user_id: int) -> User:
        # Check cache first
        if user_id in self.cache:
            return self.cache[user_id]
        
        # Query database
        user = await self.query_database(user_id)
        self.cache[user_id] = user
        return user
```

### 6. **Security**
Centralized place to implement SQL injection prevention and data validation.

```python
class UserDAL:
    async def get_user_by_id(self, user_id: int) -> User:
        # ❌ Vulnerable to SQL injection
        # query = f"SELECT * FROM users WHERE id = {user_id}"
        
        # ✅ Safe using parameterized queries
        query = "SELECT * FROM users WHERE id = %s"
        return await self.db.fetch(query, user_id)
```

---

## DAL Implementation Pattern

### Basic DAL Structure

```python
from typing import Optional, List
from app.models.user import User, UserRequest
from app.core.database import Database

class UserDAL:
    """Data Access Layer for User operations."""
    
    def __init__(self, database: Database):
        self.database = database
    
    # CREATE
    async def create_user(self, user_request: UserRequest) -> User:
        """Create a new user in the database."""
        query = """
            INSERT INTO users (name, email, phone)
            VALUES (%s, %s, %s)
            RETURNING id, name, email, phone, created_at
        """
        user_data = await self.database.fetch_one(
            query,
            (user_request.name, user_request.email, user_request.phone)
        )
        return User(**user_data)
    
    # READ
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID."""
        query = "SELECT * FROM users WHERE id = %s"
        user_data = await self.database.fetch_one(query, (user_id,))
        return User(**user_data) if user_data else None
    
    async def get_all_users(self) -> List[User]:
        """Retrieve all users."""
        query = "SELECT * FROM users ORDER BY created_at DESC"
        users_data = await self.database.fetch(query)
        return [User(**user) for user in users_data]
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email."""
        query = "SELECT * FROM users WHERE email = %s"
        user_data = await self.database.fetch_one(query, (email,))
        return User(**user_data) if user_data else None
    
    # UPDATE
    async def update_user(self, user_id: int, user_request: UserRequest) -> Optional[User]:
        """Update user information."""
        query = """
            UPDATE users 
            SET name = %s, email = %s, phone = %s
            WHERE id = %s
            RETURNING id, name, email, phone, created_at
        """
        user_data = await self.database.fetch_one(
            query,
            (user_request.name, user_request.email, user_request.phone, user_id)
        )
        return User(**user_data) if user_data else None
    
    # DELETE
    async def delete_user(self, user_id: int) -> bool:
        """Delete user by ID."""
        query = "DELETE FROM users WHERE id = %s"
        result = await self.database.execute(query, (user_id,))
        return result.rowcount > 0
```

### Service Layer Using DAL

```python
from app.repositories.user_dal import UserDAL
from app.models.user import User, UserRequest

class UserService:
    """Business logic layer using DAL."""
    
    def __init__(self, user_dal: UserDAL):
        self.user_dal = user_dal
    
    async def create_user_with_validation(self, user_request: UserRequest) -> User:
        """Create user with business logic validation."""
        # Check if user already exists
        existing = await self.user_dal.get_user_by_email(user_request.email)
        if existing:
            raise ValueError(f"User with email {user_request.email} already exists")
        
        # Create user via DAL
        user = await self.user_dal.create_user(user_request)
        
        # Additional business logic (notifications, logging, etc.)
        # await send_welcome_email(user.email)
        
        return user
    
    async def get_user_profile(self, user_id: int) -> User:
        """Get user profile with additional processing."""
        user = await self.user_dal.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Additional business logic
        # user.is_premium = await check_premium_status(user_id)
        
        return user
```

### Endpoint Using Service and DAL

```python
from fastapi import APIRouter, HTTPException
from app.services.user_service import UserService
from app.repositories.user_dal import UserDAL
from app.models.user import UserRequest, UserResponse

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/", response_model=UserResponse)
async def create_user(request: UserRequest) -> UserResponse:
    """Create a new user."""
    response = UserResponse()
    
    try:
        # Initialize DAL and Service
        dal = UserDAL(database)
        service = UserService(dal)
        
        # Call service (which uses DAL)
        user = await service.create_user_with_validation(request)
        
        response.Data = user
        response.Message = "User created successfully"
        return response
        
    except ValueError as ve:
        response.IsInvalid = True
        response.Message = {"error": str(ve)}
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": "Internal server error"}
        return response

@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    """Retrieve user by ID."""
    response = UserResponse()
    
    try:
        dal = UserDAL(database)
        service = UserService(dal)
        
        user = await service.get_user_profile(user_id)
        
        response.Data = user
        return response
        
    except ValueError as ve:
        response.IsInvalid = True
        response.Message = {"error": str(ve)}
        return response
```

---

## DAL Patterns in VishAgent

### Repository Pattern (DAL Implementation)

```python
# repositories/user_dal.py
class UserDAL:
    """Repository pattern for user data."""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def find_by_id(self, user_id: int):
        pass
    
    async def find_all(self):
        pass
    
    async def save(self, user):
        pass
    
    async def update(self, user):
        pass
    
    async def delete(self, user_id):
        pass
```

### Claim Policy DAL Example (Following VishAgent Pattern)

```python
# repositories/claim_policy_dal.py
class ClaimPolicyDAL:
    """DAL for Claim Policy operations."""
    
    async def get_claim_by_id(self, claim_id: int) -> ClaimPolicy:
        """Retrieve claim policy from database."""
        query = "SELECT * FROM claims WHERE id = %s"
        return await self.db.fetch_one(query, (claim_id,))
    
    async def create_claim(self, claim: ClaimPolicyRequest) -> ClaimPolicy:
        """Store new claim in database."""
        query = """
            INSERT INTO claims (policy_id, claim_amount, status)
            VALUES (%s, %s, %s)
            RETURNING id, policy_id, claim_amount, status, created_at
        """
        return await self.db.fetch_one(
            query,
            (claim.policy_id, claim.amount, "pending")
        )
    
    async def update_claim_status(self, claim_id: int, status: str) -> bool:
        """Update claim status after LLM processing."""
        query = "UPDATE claims SET status = %s WHERE id = %s"
        return await self.db.execute(query, (status, claim_id))
```

---

## DAL Best Practices

### 1. **Always Use Parameterized Queries**
Prevents SQL injection attacks.

```python
# ❌ Vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ Safe
query = "SELECT * FROM users WHERE id = %s"
result = await db.fetch(query, (user_id,))
```

### 2. **Handle NULL Values Properly**
```python
async def get_user_by_id(self, user_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE id = %s"
    user_data = await self.db.fetch_one(query, (user_id,))
    return User(**user_data) if user_data else None  # Check for None
```

### 3. **Use Connection Pooling**
Improves performance by reusing connections.

```python
class Database:
    def __init__(self):
        self.pool = asyncpg.create_pool(
            dsn="postgresql://user:password@localhost/db",
            min_size=10,
            max_size=20
        )
```

### 4. **Implement Caching**
Reduce database queries for frequently accessed data.

```python
class UserDAL:
    def __init__(self, db, cache=None):
        self.db = db
        self.cache = cache or {}
    
    async def get_user_by_id(self, user_id: int):
        if user_id in self.cache:
            return self.cache[user_id]
        
        user = await self._query_database(user_id)
        self.cache[user_id] = user
        return user
```

### 5. **Log Database Operations**
Track what's happening at the data layer.

```python
import logging

logger = logging.getLogger(__name__)

class UserDAL:
    async def create_user(self, user: User):
        logger.info(f"Creating user: {user.email}")
        try:
            result = await self.db.execute(query, values)
            logger.info(f"User created with ID: {result}")
            return result
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
```

### 6. **Use Transactions for Related Operations**
Ensure data consistency.

```python
async def create_order_with_items(self, order: Order, items: List[OrderItem]):
    async with self.db.transaction():
        # Both operations succeed or both fail
        order_id = await self.create_order(order)
        await self.create_order_items(order_id, items)
        return order_id
```

---

## VishAgent Project Structure with DAL

```
app/
├── api/
│   └── v1/routes/          # Endpoints
│       └── claims.py
├── services/               # Business Logic
│   └── claim_service.py
├── repositories/           # DAL Layer ← Data Access
│   ├── claim_dal.py
│   ├── user_dal.py
│   └── policy_dal.py
├── models/                 # Pydantic Models
│   ├── claim.py
│   └── user.py
└── core/
    └── database.py         # Database Connection
```

---

## Summary: DAL Importance

| Aspect | Benefit |
|--------|---------|
| **Abstraction** | Hide database complexity from business logic |
| **Testability** | Mock database without real connections |
| **Maintainability** | Change database with minimal code changes |
| **Reusability** | Share data access methods across services |
| **Security** | Centralized SQL injection prevention |
| **Performance** | Caching, connection pooling, query optimization |
| **Scalability** | Easy to add new data sources |

## Related Files

- [models/](models/) - Pydantic data models
- [core/config.py](core/config.py) - Database configuration
- [ClaimPolicy.txt](../Documents/ClaimPolicy/ClaimPolicy.txt) - Claim processing flow
- [READMEProjectStructure.md](READMEProjectStructure.md) - Architecture overview
