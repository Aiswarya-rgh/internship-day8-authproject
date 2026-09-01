# Job Portal API – Developer Guide

## 1. Overview

The Job Portal API provides authentication, job management, applications,
billing, and other platform functionality through REST APIs.

## 2. Base URL

http://54.252.215.81/

Replace YOUR-EC2-IP with the deployed EC2 public IP.

## 3. API Documentation

Interactive Swagger documentation:

/api/docs/

OpenAPI schema:

/api/schema/

## 4. Authentication

The API uses JWT authentication.

### Login

Send user credentials to:

POST /api/login/

The response provides an access token and refresh token.

### Using the Access Token

For protected endpoints, send:

Authorization: Bearer <access_token>

### Refreshing the Token

Use:

POST /api/refresh/

with the refresh token to obtain a new access token.

### Token Lifetime

Access token: 30 minutes

Refresh token: 1 day

## 5. Endpoint Documentation

Swagger UI provides the available API endpoints, HTTP methods,
request structures, authentication requirements, and response schemas.

Developers can use Swagger UI to test supported API operations.

## 6. API Keys

The current application does not use API-key authentication.
Authentication is handled using JWT Bearer tokens.

## 7. Integration Instructions

1. Open the API base URL.
2. Access /api/docs/ to view the API.
3. Authenticate using the login endpoint.
4. Save the returned access token.
5. Send the token in the Authorization header.
6. Use the refresh endpoint when the access token expires.
7. Check Swagger for endpoint-specific request and response formats.

## 8. Security

Protected endpoints require authentication and appropriate permissions.
Clients should never expose JWT tokens or other credentials publicly.
