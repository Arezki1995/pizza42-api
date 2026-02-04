# Pizza 42 API

A FastAPI-based backend for the Pizza 42 ordering application, featuring JWT-based authentication and access control.

## API Structure

The Pizza 42 API is organized into the following main components:

### Application Layout

```
app/
├── main.py                 # FastAPI app initialization and router registration
├── configuration/          # Configuration management
│   └── config.py           # Environment and settings loading
├── dependencies/           # Dependency injection dependencies
│   └── auth_scheme.py      # JWT authentication scheme
├── models/                 # Data models
│   ├── order.py            # Order model
│   └── pizza.py            # Pizza model
├── routers/                # API route handlers
│   ├── common.py           # Common routes (root redirect)
│   ├── menu.py             # Menu endpoints
│   └── orders.py           # Order endpoints
└── security/               # Security utilities
    └── jwt.py              # JWT verification logic
```

### Router Endpoints

| Router | Prefix | Endpoints |
|--------|--------|-----------|
| **menu_router** | `/menu` | Serves pizza menu items |
| **orders_router** | `/orders` | Order management (create, retrieve) |
| **common_router** | `/` | Root redirect to API docs |

Note: a static files path for images /images/ is added to host the logo and background image. This serves as a CDN to Auth0 to fetch them.

### Middleware

- **CORS Middleware**: Configured to allow requests from specified origins with Authorization and Content-Type headers

## Access Control: JWT Authentication

The API implements JWT-based authentication with scope and permissions validation.

### 1. JWT Verification (`app/security/jwt.py`)

The `VerifyJWT` class handles token validation:

**Key points:**
- Retrieves signing keys from Auth0 JWKS endpoint
- Decodes and verifies JWT signature
- Validates token claims: audience, issuer, scopes, and permissions ( for api actions we rely on the granted scopes )
- Returns standardized response structure (something that we can work with easily)

**Verification Flow:**
1. Fetches signing key from JWKS endpoint
2. Decodes token with configured algorithms and claims validation
3. Optionally verifies scopes (space-separated string) (On the wrapping layer auth_scheme.py scope is required)
4. Optionally verifies permissions (list of required permissions) (Initially used for testing with Auth0 RBAC that sets a permissions claim before migrating to post login actions that affects scopes)
5. Returns payload on success or error details on failure

**Response Format:**
```json
{
  "status": "success|error",
  "type": "error_type_or_null",
  "payload": "decoded_payload_or_error_message"
}
```

### 2. Dependency Injection (`app/dependencies/auth_scheme.py`)

The `jwt_required()` function creates a FastAPI dependency for route protection:

**How It Works:**
- Uses FastAPI's `HTTPBearer` security scheme to extract Bearer tokens from Authorization headers
- Creates a dependency factory that validates JWT claims
- Returns the decoded JWT payload for use in route handlers
- Raises `HTTP 401 Unauthorized` if verification fails

**Usage Pattern:**
```python
@router.post("/endpoint")
def protected_endpoint(
    payload: dict = Depends(jwt_required(scopes=["required:scope"]))
):
    # payload contains decoded JWT claims
    pass
```

### 3. Integration with Protected Endpoints

Protected endpoints use the `jwt_required()` dependency with specific scopes:

#### Menu Access
- **Endpoint**: `GET /menu`
- **Authentication**: None required (public endpoint)

#### Order Creation
- **Endpoint**: `POST /orders/`
- **Required Scope**: `create:orders`
- **Access**: Creates orders for authenticated users
- **User Identification**: Extracts user subject from JWT payload (`payload.get("sub")`)

#### Order Retrieval
- **Endpoint**: `GET /orders/`
- **Required Scope**: `read:orders`
- **Access**: Retrieves orders for a specific user subject


### Access Control Flow

```
HTTP Request with Authorization Header
        ↓
HTTPBearer scheme extracts Bearer token
        ↓
jwt_required() dependency invoked with required scopes
        ↓
VerifyJWT class verifies token signature and claims
        ↓
If valid → decoded payload passed to route handler
If invalid → HTTP 401 Unauthorized response
```

## Authentication Configuration

JWT verification uses configuration from environment variables:
- `DOMAIN`: Auth0 domain (for JWKS endpoint)
- `API_AUDIENCE`: Expected token audience
- `ISSUER`: Expected token issuer
- `ALGORITHMS`: Token signing algorithms

## Prerequisites

- Python 3.8+
- FastAPI
- PyJWT with PyJWKClient
- CORS middleware support
