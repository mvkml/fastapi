# VishAgent - User API Endpoints Documentation

## Overview

The User API provides comprehensive REST endpoints for managing user data following the **API → Service → DAL** architectural pattern. All endpoints are type-safe, well-documented, and include comprehensive error handling.

### API Base Path
```
/api/users
```

---

## User Endpoints

### 1. Health Check

**Endpoint**: `GET /api/users`

**Description**: Verify user API is operational

**Response**:
```json
{
  "message": "User API is operational",
  "status": "ok"
}
```

**Implementation**:
```python
@user_router.get("")
async def default_user():
    """Health check endpoint for user API."""
    return {"message": "User API is operational", "status": "ok"}
```

---

### 2. Get Single User

**Endpoint**: `GET /api/users/{user_id}`

**Description**: Retrieve a single user by ID

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| user_id | integer | Unique identifier of the user |

**Request Example**:
```http
GET /api/users/1
```

**Response Model** (UserResponse):
```json
{
  "IsInvalid": false,
  "Message": "User retrieved successfully",
  "Data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "created_at": "2024-01-14T10:30:00"
  }
}
```

**Error Response**:
```json
{
  "IsInvalid": true,
  "Message": {
    "error": "User 1 not found"
  },
  "Data": null
}
```

**Implementation Pattern**:
```python
@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    response = UserResponse()
    try:
        dal = UserDAL()
        service = UserService(dal)
        user = await service.get_user(user_id)
        
        response.Data = user
        response.Message = "User retrieved successfully"
        return response
        
    except ValueError as ve:
        response.IsInvalid = True
        response.Message = {"error": str(ve)}
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": "Internal server error"}
        return response
```

---

### 3. Get All Users

**Endpoint**: `GET /api/users`

**Description**: Retrieve all users with pagination support

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| skip | integer | 0 | Number of records to skip |
| limit | integer | 10 | Maximum number of records to return |

**Request Examples**:
```http
GET /api/users?skip=0&limit=10
GET /api/users?skip=10&limit=20
```

**Response Model**:
```json
{
  "IsInvalid": false,
  "Message": "Retrieved 5 users",
  "Data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "555-1234",
      "created_at": "2024-01-14T10:30:00"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "555-5678",
      "created_at": "2024-01-13T15:45:00"
    }
  ]
}
```

**Implementation Pattern**:
```python
@user_router.get("/", response_model=UserResponse)
async def get_users(skip: int = 0, limit: int = 10) -> UserResponse:
    response = UserResponse()
    try:
        dal = UserDAL()
        service = UserService(dal)
        users = await service.get_all_users(skip, limit)
        
        response.Data = users
        response.Message = f"Retrieved {len(users)} users"
        return response
        
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": "Internal server error"}
        return response
```

---

### 4. Create User

**Endpoint**: `POST /api/users`

**Description**: Create a new user

**Request Body** (UserRequest):
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234"
}
```

**Request Example**:
```http
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234"
}
```

**Success Response** (201 Created):
```json
{
  "IsInvalid": false,
  "Message": "User created successfully",
  "Data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "created_at": "2024-01-14T10:30:00"
  }
}
```

**Validation Error Response**:
```json
{
  "IsInvalid": true,
  "Message": {
    "validation_error": "User with email john@example.com already exists"
  },
  "Data": null
}
```

**Implementation Pattern**:
```python
@user_router.post("/", response_model=UserResponse)
async def create_user(request: UserRequest) -> UserResponse:
    response = UserResponse()
    try:
        dal = UserDAL()
        service = UserService(dal)
        user = await service.create_user(request)
        
        response.Data = user
        response.Message = "User created successfully"
        return response
        
    except ValueError as ve:
        response.IsInvalid = True
        response.Message = {"validation_error": str(ve)}
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": "Internal server error"}
        return response
```

---

### 5. Update User

**Endpoint**: `PUT /api/users/{user_id}`

**Description**: Update an existing user's information

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| user_id | integer | ID of user to update |

**Request Body** (UserRequest):
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "555-5678"
}
```

**Request Example**:
```http
PUT /api/users/1
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "555-5678"
}
```

**Success Response**:
```json
{
  "IsInvalid": false,
  "Message": "User updated successfully",
  "Data": {
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "555-5678",
    "created_at": "2024-01-14T10:30:00"
  }
}
```

**Implementation Pattern**:
```python
@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, request: UserRequest) -> UserResponse:
    response = UserResponse()
    try:
        dal = UserDAL()
        service = UserService(dal)
        user = await service.update_user(user_id, request)
        
        response.Data = user
        response.Message = "User updated successfully"
        return response
        
    except ValueError as ve:
        response.IsInvalid = True
        response.Message = {"error": str(ve)}
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": "Internal server error"}
        return response
```

---

### 6. Delete User

**Endpoint**: `DELETE /api/users/{user_id}`

**Description**: Delete a user by ID

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| user_id | integer | ID of user to delete |

**Request Example**:
```http
DELETE /api/users/1
```

**Success Response**:
```json
{
  "IsInvalid": false,
  "Message": "User deleted successfully",
  "Data": null
}
```

**Error Response** (User Not Found):
```json
{
  "IsInvalid": true,
  "Message": {
    "error": "User 1 not found"
  },
  "Data": null
}
```

**Implementation Pattern**:
```python
@user_router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int) -> UserResponse:
    response = UserResponse()
    try:
        dal = UserDAL()
        service = UserService(dal)
        success = await service.delete_user(user_id)
        
        if success:
            response.Message = "User deleted successfully"
        else:
            response.IsInvalid = True
            response.Message = {"error": f"User {user_id} not found"}
        
        return response
        
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": "Internal server error"}
        return response
```

---

### 7. Upsert User

**Endpoint**: `PATCH /api/users/{user_id}`

**Description**: Create or update a user (upsert pattern)

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| user_id | integer | ID of user to create/update |

**Request Body** (UserRequest):
```json
{
  "name": "Updated Name",
  "email": "updated@example.com",
  "phone": "555-9999"
}
```

**Request Example**:
```http
PATCH /api/users/1
Content-Type: application/json

{
  "name": "Updated Name",
  "email": "updated@example.com",
  "phone": "555-9999"
}
```

**Response** (Create or Update):
```json
{
  "IsInvalid": false,
  "Message": "User created/updated successfully",
  "Data": {
    "id": 1,
    "name": "Updated Name",
    "email": "updated@example.com",
    "phone": "555-9999",
    "created_at": "2024-01-14T10:30:00"
  }
}
```

**Implementation Pattern**:
```python
@user_router.patch("/{user_id}", response_model=UserResponse)
async def upsert_user(user_id: int, request: UserRequest) -> UserResponse:
    response = UserResponse()
    try:
        dal = UserDAL()
        service = UserService(dal)
        user = await service.upsert_user(user_id, request)
        
        response.Data = user
        response.Message = "User created/updated successfully"
        return response
        
    except ValueError as ve:
        response.IsInvalid = True
        response.Message = {"error": str(ve)}
        return response
    except Exception as ex:
        response.IsInvalid = True
        response.Message = {"error": "Internal server error"}
        return response
```

---

## Response Models

### UserResponse
Used for all API responses with consistent structure:

```python
class UserResponse(BaseModel):
    """Standard response model for user operations."""
    IsInvalid: bool = False
    Message: Optional[str | dict] = None
    Data: Optional[UserModel] = None
```

### UserRequest
Used for create/update operations:

```python
class UserRequest(BaseModel):
    """Request model for user operations."""
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    phone: Optional[str] = Field(None, description="User's phone number")
```

### UserModel
Represents a complete user object:

```python
class UserModel(BaseModel):
    """Complete user model."""
    id: Optional[int] = None
    name: str
    email: str
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
```

---

## Architecture Pattern

All user endpoints follow the **3-Layer Architecture**:

```
┌─────────────────────────────────────┐
│  API Layer (api_user.py)            │  ← Endpoints
│  Request validation, response       │
├─────────────────────────────────────┤
│  Service Layer (user_service.py)    │  ← Business Logic
│  Validation, transaction management │
├─────────────────────────────────────┤
│  DAL Layer (user_dal.py)            │  ← Data Access
│  Database queries, CRUD operations  │
└─────────────────────────────────────┘
```

### Flow Example (Create User):

```
1. POST /api/users
   ↓ (UserRequest validation)
2. create_user() in api_user.py
   ↓ (Initialize layers)
3. UserDAL() + UserService(dal)
   ↓ (Call service method)
4. service.create_user(request)
   ↓ (Business logic validation)
5. dal.create_user(user_request)
   ↓ (Execute INSERT query)
6. Database INSERT
   ↓ (Return created user)
7. User object → UserResponse
   ↓ (Serialize to JSON)
8. HTTP 200 OK + Response JSON
```

---

## Error Handling Strategy

All endpoints use consistent error handling:

```python
try:
    # Step 1: Initialize DAL and Service
    dal = UserDAL()
    service = UserService(dal)
    
    # Step 2: Execute business logic
    result = await service.operation(params)
    
    # Step 3: Build success response
    response.Data = result
    response.Message = "Operation successful"
    return response
    
except ValueError as ve:
    # Handle validation errors
    response.IsInvalid = True
    response.Message = {"error": str(ve)}
    return response
    
except Exception as ex:
    # Handle unexpected errors
    response.IsInvalid = True
    response.Message = {"error": "Internal server error"}
    return response
```

### Error Types

| Error Type | HTTP Code | Use Case |
|-----------|-----------|----------|
| ValueError | 200 (in body) | Validation errors, business logic violations |
| Exception | 200 (in body) | Unexpected errors |
| IsInvalid = True | 200 | Structured error response |

---

## Usage Examples

### Using cURL

```bash
# Get single user
curl -X GET http://localhost:825/api/users/1

# Get all users with pagination
curl -X GET "http://localhost:825/api/users?skip=0&limit=10"

# Create user
curl -X POST http://localhost:825/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234"
  }'

# Update user
curl -X PUT http://localhost:825/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "555-5678"
  }'

# Delete user
curl -X DELETE http://localhost:825/api/users/1

# Upsert user
curl -X PATCH http://localhost:825/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "email": "updated@example.com",
    "phone": "555-9999"
  }'
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:825/api/users"

# Get single user
response = requests.get(f"{BASE_URL}/1")
print(response.json())

# Create user
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234"
}
response = requests.post(BASE_URL, json=user_data)
print(response.json())

# Update user
response = requests.put(f"{BASE_URL}/1", json=user_data)
print(response.json())

# Delete user
response = requests.delete(f"{BASE_URL}/1")
print(response.json())
```

---

## Best Practices Applied

1. **Type Safety**: All parameters and responses are type-annotated
2. **Async/Await**: Non-blocking I/O for better performance
3. **Proper HTTP Methods**: GET, POST, PUT, DELETE, PATCH used correctly
4. **Consistent Response Format**: All responses use UserResponse model
5. **Comprehensive Error Handling**: Try-except blocks with specific error types
6. **Logging**: Info, warning, and error level logging
7. **Documentation**: Detailed docstrings on all endpoints
8. **Pagination**: Query parameters for result limiting
9. **Separation of Concerns**: API → Service → DAL layers
10. **RESTful Design**: Resource-oriented URL structure

---

## Related Files

- [api_user.py](api/api_mange_user/api_user.py) - User endpoint implementation
- [user_service.py](../services/user_service.py) - User business logic
- [user_dal.py](../repositories/user_dal.py) - User data access
- [user_model.py](models/user_model.py) - User data models
