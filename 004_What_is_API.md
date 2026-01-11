# What is an API?

## Definition

**API** stands for **Application Programming Interface**. It is a set of rules, protocols, and tools that allows different software applications to communicate with each other.

An API acts as an intermediary that enables two applications to request and exchange data or functionality in a standardized way.

## Simple Analogy

Think of an API like a **restaurant menu**:

- **Restaurant Kitchen** = Backend system/database
- **Menu** = API documentation
- **Waiter** = API
- **Customer** = Your application

When you order food (make a request), the waiter takes your order to the kitchen and brings back your meal (response). You don't need to know how food is prepared in the kitchen—you just follow the menu's format.

## How APIs Work

```
Client Application
        |
        | (Request)
        v
    ┌─────────┐
    │   API   │
    └─────────┘
        |
        | (Response)
        v
    Backend/Service
        |
        v
    Database/Server
```

### The Process:

1. **Client Makes Request**: Application sends a request to the API with specific parameters
2. **API Processes Request**: API receives request, validates it, and processes the data
3. **Backend Logic**: API communicates with backend services/databases
4. **Prepares Response**: API formats the data according to API specifications
5. **Sends Response**: Response is sent back to the client application

## Types of APIs

### 1. Web APIs (REST APIs)

**REST** = Representational State Transfer

Most common type of API used for web communication.

**Characteristics**:
- Uses HTTP/HTTPS protocols
- Standard HTTP methods: GET, POST, PUT, DELETE, PATCH
- Returns data in JSON or XML format
- Stateless (each request is independent)
- Base URL + Endpoints

**Example REST API Structure**:
```
Base URL: https://api.example.com/v1

Endpoints:
GET    /users              - Get all users
GET    /users/{id}         - Get specific user
POST   /users              - Create new user
PUT    /users/{id}         - Update user
DELETE /users/{id}         - Delete user
```

### 2. SOAP APIs

**SOAP** = Simple Object Access Protocol

- Older web service standard
- Uses XML for messaging
- More complex than REST
- Built-in security features
- Less commonly used in modern development

### 3. GraphQL APIs

- Query language for APIs
- Request only the data you need
- Single endpoint, flexible queries
- Growing in popularity

### 4. RPC APIs

**RPC** = Remote Procedure Call

- Call functions on remote servers
- Simpler than REST for specific use cases
- Less structured

### 5. Webhooks

- Event-driven APIs
- Server pushes data to your application
- Used for notifications and real-time updates

## REST API Concepts

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|-----------|------|
| GET | Retrieve data | Yes | Yes |
| POST | Create new resource | No | No |
| PUT | Update existing resource (full) | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

### HTTP Status Codes

| Code | Category | Meaning |
|------|----------|---------|
| 2xx | Success | Request successful |
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful, no response body |
| 3xx | Redirection | Further action needed |
| 4xx | Client Error | Invalid request |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource doesn't exist |
| 5xx | Server Error | Server failed to process |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Server temporarily unavailable |

## Real-World API Examples

### 1. Google Maps API
```
Request: Get directions from Point A to Point B
Response: Route, distance, time, turn-by-turn directions
```

### 2. Twitter API
```
Request: Get tweets from a specific user
Response: Array of tweets with metadata
```

### 3. Payment Gateway (Stripe/PayPal)
```
Request: Process payment with amount and card details
Response: Transaction confirmation or error
```

### 4. Weather API
```
Request: Get weather for a city
Response: Temperature, humidity, forecast data
```

### 5. Social Login API
```
Request: Authenticate user with Google/Facebook
Response: User credentials and profile information
```

## API Request & Response Example

### Request
```http
GET /api/users/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer token_xyz
Content-Type: application/json
```

### Response
```json
{
  "id": 123,
  "name": "Vishnu Kiran",
  "email": "vishnu@example.com",
  "role": "Enterprise AI Designer",
  "created_at": "2024-01-11T10:30:00Z"
}
```

## Key API Characteristics

### 1. **Endpoints**
Specific URLs that perform specific functions

### 2. **Parameters**
Input data passed to the API (query params, body, headers)

### 3. **Authentication**
Verification mechanism (API keys, OAuth, tokens)

### 4. **Rate Limiting**
Restrictions on number of requests per time period

### 5. **Documentation**
Clear instructions on how to use the API

### 6. **Error Handling**
Clear error messages and status codes

### 7. **Versioning**
Different API versions for backward compatibility

## Why APIs Matter

### 1. **Modularity**
Break applications into independent, reusable components

### 2. **Integration**
Connect different systems and services seamlessly

### 3. **Scalability**
Scale components independently

### 4. **Security**
Control access to data and functionality

### 5. **Flexibility**
Clients can use APIs in different ways

### 6. **Standardization**
Common interface for all clients

### 7. **Third-Party Integration**
Allow external developers to build on your platform

## API Security

### Authentication Methods

**API Key**:
```
Authorization: Bearer your-api-key-here
```

**OAuth 2.0**:
```
- User logs in through provider
- Provider grants token
- Token used for subsequent requests
```

**JWT (JSON Web Token)**:
```
- Token contains user information
- Token signature ensures authenticity
- Stateless authentication
```

## FastAPI for Building APIs

FastAPI is a modern Python framework specifically designed for building APIs:

```python
from fastapi import FastAPI

app = FastAPI()

# Define an endpoint
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {
        "user_id": user_id,
        "name": "Vishnu Kiran",
        "role": "Enterprise AI Designer"
    }

# Automatic documentation generated
# Swagger UI: /docs
# ReDoc: /redoc
```

**FastAPI Benefits**:
- Fast performance
- Automatic API documentation
- Type hints with Pydantic validation
- Easy to use and learn
- Production-ready

## API Best Practices

### 1. **RESTful Design**
Follow REST principles for consistency

### 2. **Versioning**
- Use URL versioning: `/v1/`, `/v2/`
- Or header versioning: `API-Version: 2`

### 3. **Clear Documentation**
- Document all endpoints
- Provide request/response examples
- List error codes

### 4. **Consistent Naming**
- Use lowercase for URLs
- Use hyphens for multi-word endpoints
- Plural nouns for collections

### 5. **Pagination**
For large datasets, use pagination:
```
GET /api/users?page=1&limit=10
```

### 6. **Error Responses**
```json
{
  "error": "Resource not found",
  "code": 404,
  "message": "User with ID 123 does not exist"
}
```

### 7. **Rate Limiting**
Prevent abuse with rate limits

### 8. **CORS (Cross-Origin Resource Sharing)**
Handle requests from different domains

## Common API Use Cases

1. **Mobile Applications**: Fetch data from backend server
2. **Web Applications**: Load dynamic data without page refresh
3. **Microservices**: Communication between services
4. **IoT Devices**: Send sensor data to servers
5. **Third-Party Integration**: Connect with external services
6. **Real-Time Updates**: Webhooks and WebSockets
7. **Data Access**: Provide controlled access to databases

## API Lifecycle

```
1. Design       → Plan API structure and endpoints
2. Development  → Build API using framework (FastAPI)
3. Testing      → Test endpoints and edge cases
4. Documentation → Create clear documentation
5. Deployment   → Deploy to production
6. Monitoring   → Monitor performance and errors
7. Maintenance  → Update and improve API
```

## Conclusion

An **API is the bridge** between applications, enabling them to communicate and share data efficiently. Whether you're building a simple microservice or a complex enterprise application, understanding APIs is fundamental to modern software development.

FastAPI makes building powerful, scalable APIs simple and enjoyable, with automatic documentation and high performance out of the box.

---

## Profile

**Name:** Vishnu Kiran M

**Role:** Enterprise AI End to End Designer

**Focus:** Designing and implementing comprehensive AI solutions across the enterprise stack, from concept to deployment.

**Expertise:** Building scalable APIs, designing enterprise AI systems, and creating end-to-end solutions for production environments.

ViKi Pedia
