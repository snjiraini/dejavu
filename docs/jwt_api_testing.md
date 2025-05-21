# JWT API Authentication Testing Guide

This document provides instructions on how to test the JWT (JSON Web Token) authentication for the Dejavu API using curl.

## Prerequisites

- cURL command-line tool
- Running Dejavu web application (Django server)

## Testing Steps

### 1. Obtain a JWT Token

To authenticate with the API, you first need to obtain a JWT token by providing valid credentials:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"adminpassword"}' http://localhost:8000/api/token/
```

**Sample Output:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NzkzOTI5NywiaWF0IjoxNzQ3ODUyODk3LCJqdGkiOiIzYmU0ZTUxNDFiYmQ0MGM2YmI4ZTk3ODllOTJjNGQxMiIsInVzZXJfaWQiOjF9.I85kIoJVH4925WsZ2KtTLdv87axd3uJytySIRFRsLM0",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3ODU2NDk3LCJpYXQiOjE3NDc4NTI4OTcsImp0aSI6IjdjOGY1ODRjZTU4ODQyYzdiNTI0NWJkOGM3OWJhMjM4IiwidXNlcl9pZCI6MX0.RI3-IQEEUWbAVjjUkYQxF5D-CPgz4qmlDGujlZfqeuE"
}
```

The response contains two tokens:

- `access`: The access token to use for authentication (valid for 1 hour)
- `refresh`: The refresh token to use for obtaining new access tokens (valid for 1 day)

### 2. Use the Access Token to Access Protected Resources

#### Get Current User Info

```bash
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3ODU2NDk3LCJpYXQiOjE3NDc4NTI4OTcsImp0aSI6IjdjOGY1ODRjZTU4ODQyYzdiNTI0NWJkOGM3OWJhMjM4IiwidXNlcl9pZCI6MX0.RI3-IQEEUWbAVjjUkYQxF5D-CPgz4qmlDGujlZfqeuE"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/auth/me/
```

**Sample Output:**

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "roles": ["superuser"],
  "is_superuser": true
}
```

#### List Users (Superuser Only)

```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/auth/users/list/
```

Sample output would include a list of all users in the system.

### 3. Refresh the Access Token

When the access token expires, you can use the refresh token to obtain a new access token:

```bash
export REFRESH_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NzkzOTI5NywiaWF0IjoxNzQ3ODUyODk3LCJqdGkiOiIzYmU0ZTUxNDFiYmQ0MGM2YmI4ZTk3ODllOTJjNGQxMiIsInVzZXJfaWQiOjF9.I85kIoJVH4925WsZ2KtTLdv87axd3uJytySIRFRsLM0"
curl -X POST -H "Content-Type: application/json" -d "{\"refresh\":\"$REFRESH_TOKEN\"}" http://localhost:8000/api/token/refresh/
```

**Expected Sample Output:**

```json
{ "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }
```

## Testing with Different User Roles

### Artist User

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"artist1","password":"password123"}' http://localhost:8000/api/token/
```

**Sample Output for Artist Login:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Use the obtained token to access artist-specific resources.

## Running the Server

Before testing, make sure the Django server is running:

```bash
cd /workspace/dejavu_web
python manage.py runserver 0.0.0.0:8000
```

The server will start and output something like:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 21, 2023 - 14:32:55
Django version 3.2.25, using settings 'dejavu_web.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

## Error Cases to Test

### Invalid Credentials

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"wrongpassword"}' http://localhost:8000/api/token/
```

**Sample Output:**

```json
{ "detail": "No active account found with the given credentials" }
```

### Accessing Protected Endpoint without Token

```bash
curl http://localhost:8000/api/auth/me/
```

**Sample Output:**

```json
{ "detail": "Authentication credentials were not provided." }
```

### Accessing Endpoint with Expired Token

When using an expired token:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.EXPIRED_TOKEN" http://localhost:8000/api/auth/me/
```

**Sample Output:**

```json
{ "detail": "Token is invalid or expired", "code": "token_not_valid" }
```

## Role-Based Access Testing

Test that users can only access endpoints they have permission for:

1. Login as artist1 user and get token
2. Try to access superuser-only endpoints (should receive 403 Forbidden)

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"artist1","password":"password123"}' http://localhost:8000/api/token/
export ARTIST_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # Use the actual token from the response
curl -H "Authorization: Bearer $ARTIST_TOKEN" http://localhost:8000/api/auth/users/list/
```

**Sample Output:**

```json
{ "error": "Access forbidden. Required roles: superuser" }
```
