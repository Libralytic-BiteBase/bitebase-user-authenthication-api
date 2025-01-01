# Auth API

## Overview
The Auth API provides authentication and authorization functionalities for your application. This guide will help you understand how to use the API effectively.

## Base URL
```
https://api.example.com/v1
```

## Authentication
All endpoints require an API key. You can obtain your API key by signing up on our platform.

## Endpoints

### 1. Register
**Endpoint:** `/auth/register`

**Method:** `POST`

**Description:** Registers a new user.

**Request:**
```json
{
    "username": "your_username",
    "password": "your_password",
    "email": "your_email@example.com"
}
```

**Response:**
```json
{
    "message": "User registered successfully",
    "userId": "unique_user_id"
}
```

### 2. Login
**Endpoint:** `/auth/login`

**Method:** `POST`

**Description:** Authenticates a user and returns a token.

**Request:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "token": "your_jwt_token"
}
```

### 3. Get User Info
**Endpoint:** `/auth/user`

**Method:** `GET`

**Description:** Retrieves information about the authenticated user.

**Headers:**
```
Authorization: Bearer your_jwt_token
```

**Response:**
```json
{
    "userId": "unique_user_id",
    "username": "your_username",
    "email": "your_email@example.com"
}
```

## Error Handling
The API uses standard HTTP status codes to indicate the success or failure of an API request. Common status codes include:
- `200 OK`: The request was successful.
- `400 Bad Request`: The request was invalid or cannot be served.
- `401 Unauthorized`: Authentication failed or user does not have permissions.
- `500 Internal Server Error`: An error occurred on the server.

## Example Usage
Here is an example of how to use the Auth API with `curl`:

```sh
# Register a new user
curl -X POST https://api.example.com/v1/auth/register \
    -H "Content-Type: application/json" \
    -d '{"username": "your_username", "password": "your_password", "email": "your_email@example.com"}'

# Login
curl -X POST https://api.example.com/v1/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username": "your_username", "password": "your_password"}'

# Get user info
curl -X GET https://api.example.com/v1/auth/user \
    -H "Authorization: Bearer your_jwt_token"
```

## Contact
For any questions or issues, please contact our support team at support@example.com.
# BiteBase-Restuarant-Dashboard-Backend
