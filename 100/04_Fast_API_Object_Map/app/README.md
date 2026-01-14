# VishAgent - Map Utility and Mapping Objects

## What is the Map Utility?

The **Map Utility** is a programming pattern that transforms data from one structure to another. In Python, the `map()` function is a built-in utility that applies a function to every item of an iterable (list, tuple, etc.) and returns an iterator with the results.

### Basic Map Function

```python
# Syntax
map(function, iterable)

# Example
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, numbers)
result = list(squared)  # [1, 4, 9, 16, 25]
```

---

## What is the Use of Mapping Objects?

**Mapping objects** are used to transform data between different representations or structures. They serve several key purposes:

### 1. **Data Transformation**
Convert data from one format to another

```python
# Transform list of integers to strings
numbers = [1, 2, 3]
strings = list(map(str, numbers))  # ['1', '2', '3']
```

### 2. **Data Extraction**
Extract specific fields from complex objects

```python
users = [
    {"id": 1, "name": "John", "email": "john@example.com"},
    {"id": 2, "name": "Jane", "email": "jane@example.com"}
]

# Extract only names
names = list(map(lambda user: user['name'], users))
# Result: ['John', 'Jane']
```

### 3. **Object Conversion**
Convert between different object types

```python
# Convert dictionaries to Pydantic models
class UserModel(BaseModel):
    id: int
    name: str

user_dicts = [{"id": 1, "name": "John"}]
user_models = list(map(UserModel, user_dicts))
```

---

## Mapping in VishAgent Architecture

In VishAgent, mapping is crucial for converting data between layers:

### API → Service → DAL Flow

```
HTTP Request (JSON)
    ↓ [Pydantic Validation]
UserRequest (Pydantic Model)
    ↓ [Mapping/Transformation]
User (Domain Model)
    ↓ [Service Processing]
User (with additional fields)
    ↓ [DAL Mapping]
Database Record
```

---

## Practical Mapping Examples in VishAgent

### 1. Request to Domain Model Mapping

```python
# api_user.py
@user_router.post("/")
async def create_user(request: UserRequest) -> UserResponse:
    """
    Request: UserRequest (from API)
    Maps to: User (domain model)
    """
    dal = UserDAL()
    service = UserService(dal)
    
    # Map UserRequest to domain model
    user = await service.create_user(request)
    
    # Map User to UserResponse
    response.Data = user
    return response
```

### 2. Database Record to Model Mapping

```python
# repositories/user_dal.py
async def get_user_by_id(self, user_id: int) -> Optional[User]:
    """Map database record to User model"""
    query = "SELECT * FROM users WHERE id = %s"
    result = await self.db.fetch_one(query, (user_id,))
    
    # Map database row to User model
    return User(**result) if result else None
```

### 3. Multiple Records Mapping

```python
# Use map() to transform multiple objects
async def get_all_users(self) -> List[User]:
    """Map multiple database records to User models"""
    query = "SELECT * FROM users"
    results = await self.db.fetch(query)
    
    # Method 1: Using list comprehension (preferred)
    return [User(**row) for row in results]
    
    # Method 2: Using map()
    return list(map(User, results))
```

---

## Map vs List Comprehension

### Using map()
```python
numbers = [1, 2, 3, 4, 5]

# map() - returns iterator
result_map = map(lambda x: x * 2, numbers)
print(list(result_map))  # [2, 4, 6, 8, 10]
```

### Using List Comprehension (Preferred in Python)
```python
numbers = [1, 2, 3, 4, 5]

# List comprehension - more Pythonic
result_list = [x * 2 for x in numbers]
print(result_list)  # [2, 4, 6, 8, 10]
```

### Comparison

| Aspect | map() | List Comprehension |
|--------|-------|-------------------|
| **Readability** | Less Pythonic | More Pythonic |
| **Performance** | Lazy evaluation | Eager evaluation |
| **Memory** | Lower (iterator) | Higher (full list) |
| **Flexibility** | Single function | Complex logic |
| **Debugging** | Harder | Easier |

---

## Mapping Objects in VishAgent: DTOs and Models

### 1. Request Model Mapping

```python
# models/user_model.py
class UserRequest(BaseModel):
    """API Request DTO"""
    name: str
    email: str
    phone: Optional[str] = None

class UserModel(BaseModel):
    """Domain Model"""
    id: Optional[int] = None
    name: str
    email: str
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Map from ORM objects

# Mapping UserRequest to UserModel
request = UserRequest(name="John", email="john@example.com")
user_model = UserModel(**request.dict())
```

### 2. Database to Model Mapping

```python
# Pydantic from_attributes enables mapping from ORM/database objects
class UserModel(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True  # Maps database row directly

# When database returns a row as dict or object
db_row = {"id": 1, "name": "John", "email": "john@example.com"}
user = UserModel(**db_row)  # Automatic mapping
```

### 3. Model to Response Mapping

```python
# services/user_service.py
async def get_user(self, user_id: int) -> UserModel:
    """
    Service returns domain model
    API converts to response format
    """
    user = await self.dal.get_user_by_id(user_id)
    return user  # UserModel

# api_user.py - Convert to response
response.Data = user  # UserModel → included in UserResponse
return response  # Response is serialized to JSON
```

---

## Advanced Mapping Patterns

### 1. Custom Mapping Functions

```python
# utils/mappers.py
def map_user_to_response(user: UserModel) -> dict:
    """Custom mapping function"""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "profile": f"{user.name} ({user.email})"
    }

# Usage
user = UserModel(id=1, name="John", email="john@example.com")
response_data = map_user_to_response(user)
```

### 2. Mapper Class Pattern

```python
# utils/mappers.py
class UserMapper:
    """Centralized mapping logic"""
    
    @staticmethod
    def to_model(user_request: UserRequest) -> UserModel:
        """Map request to domain model"""
        return UserModel(**user_request.dict())
    
    @staticmethod
    def to_response(user: UserModel) -> dict:
        """Map domain model to response"""
        return user.dict(exclude={"created_at"})
    
    @staticmethod
    def to_db(user: UserModel) -> dict:
        """Map domain model to database format"""
        return user.dict(exclude={"id"})

# Usage
request = UserRequest(name="John", email="john@example.com")
user = UserMapper.to_model(request)
response = UserMapper.to_response(user)
```

### 3. Batch Mapping with map()

```python
# Apply transformation to collection
users_data = [
    {"id": 1, "name": "John", "email": "john@example.com"},
    {"id": 2, "name": "Jane", "email": "jane@example.com"}
]

# Option 1: Using map()
users = list(map(lambda d: UserModel(**d), users_data))

# Option 2: Using list comprehension (preferred)
users = [UserModel(**d) for d in users_data]
```

---

## Mapping Use Cases in VishAgent

### Use Case 1: API Request Processing

```
1. HTTP Request (JSON string)
   ↓
2. FastAPI deserialization (UserRequest Pydantic model)
   ↓
3. Service layer (map to domain model)
   ↓
4. Business logic processing
   ↓
5. Response mapping (UserModel to UserResponse)
   ↓
6. HTTP Response (JSON string)
```

### Use Case 2: Data Retrieval

```
1. Database query returns raw data
   ↓
2. DAL maps to domain model (UserModel)
   ↓
3. Service adds business context
   ↓
4. API maps to response format
   ↓
5. Returns serialized JSON
```

### Use Case 3: Multi-Record Processing

```python
# Get all users and map to response format
async def get_all_users(self) -> UserResponse:
    dal = UserDAL()
    service = UserService(dal)
    
    # Get list of UserModel objects
    users = await service.get_all_users()
    
    # Map to response format (implicit - Pydantic handles it)
    response.Data = users
    return response
```

---

## Best Practices for Mapping in VishAgent

### 1. **Use Pydantic for Automatic Mapping**
```python
# ✅ Preferred - Pydantic handles validation and mapping
class UserModel(BaseModel):
    id: int
    name: str
    email: str

user = UserModel(**database_row)  # Automatic mapping
```

### 2. **Prefer List Comprehension over map()**
```python
# ❌ Avoid
users = list(map(UserModel, db_rows))

# ✅ Preferred
users = [UserModel(**row) for row in db_rows]
```

### 3. **Centralize Mapping Logic**
```python
# ✅ Good - Mapping logic in one place
class UserMapper:
    @staticmethod
    def to_model(request: UserRequest) -> UserModel:
        return UserModel(**request.dict())

# Use in multiple places
user = UserMapper.to_model(request)
```

### 4. **Type Hints for Clarity**
```python
# ✅ Good - Clear input/output types
def map_to_response(user: UserModel) -> dict:
    """Maps UserModel to response dictionary"""
    return user.dict()

# ❌ Avoid - Ambiguous
def map_data(data):
    return data
```

### 5. **Separate Concerns**
```python
# ✅ Good - Each layer handles its own mapping
# API layer: Request → Domain Model
# Service layer: Domain Model → Enriched Model
# DAL layer: Enriched Model → Database format
```

---

## Performance Considerations

### Memory Usage

```python
# map() - Lazy evaluation (lower memory for large datasets)
large_list = range(1000000)
result = map(lambda x: x * 2, large_list)  # Not evaluated yet
first_item = next(result)  # Only one item evaluated

# List comprehension - Eager evaluation (full list in memory)
result = [x * 2 for x in large_list]  # All evaluated immediately
```

### When to Use map()
- Processing large datasets
- Need lazy evaluation
- Single simple transformation

### When to Use List Comprehension
- Small to medium datasets
- Complex transformations
- Need full list in memory anyway
- Code readability is priority

---

## Mapping Objects in VishAgent DTOs

### Complete Example

```python
# models/user_model.py
class UserRequest(BaseModel):
    """Request DTO - from API client"""
    name: str
    email: str
    phone: Optional[str] = None

class UserModel(BaseModel):
    """Domain Model - internal representation"""
    id: Optional[int] = None
    name: str
    email: str
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    """Response DTO - to API client"""
    IsInvalid: bool = False
    Message: Optional[str | dict] = None
    Data: Optional[UserModel] = None

# services/user_service.py
class UserService:
    async def create_user(self, request: UserRequest) -> UserModel:
        # Map request to model
        user_data = request.dict()
        user = UserModel(**user_data)
        
        # Process via DAL
        created = await self.dal.create_user(user)
        return created

# api_user.py
@user_router.post("/", response_model=UserResponse)
async def create_user(request: UserRequest) -> UserResponse:
    response = UserResponse()
    try:
        dal = UserDAL()
        service = UserService(dal)
        
        # Service returns UserModel
        user = await service.create_user(request)
        
        # Map to response
        response.Data = user  # UserModel
        response.Message = "User created"
        return response  # Pydantic serializes to JSON
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": str(ex)}
        return response
```

---

## Summary

| Concept | Purpose | Use in VishAgent |
|---------|---------|------------------|
| **Map Utility** | Transform each item in a collection | Process collections efficiently |
| **Mapping Objects** | Convert between different data structures | Transform data between API/Service/DAL layers |
| **Pydantic Models** | Automatic validation and mapping | Request/response DTOs |
| **List Comprehension** | Readable transformation syntax | Preferred over map() |
| **Custom Mappers** | Centralized mapping logic | Reusable mapping functions |

---

## Related Files

- [api/api_mange_user/api_user.py](api/api_mange_user/api_user.py) - Mapping in API layer
- [models/user_model.py](models/user_model.py) - Data models for mapping
- [services/user_service.py](services/user_service.py) - Mapping in service layer
- [repositories/user_dal.py](repositories/user_dal.py) - Mapping in DAL layer
