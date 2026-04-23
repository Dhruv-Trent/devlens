# DevLens

DevLens is an AI-powered web application that helps developers understand and improve codebases.

## Tech Stack

* Frontend: Next.js + TypeScript + Tailwind CSS
* Backend: FastAPI + Python
* Database: PostgreSQL
* Containers: Docker + Docker Compose

## Day 1 Setup Complete

Current progress:

* Frontend initialized
* Backend initialized
* PostgreSQL added
* Docker Compose added
* Health check endpoint working

## Day 2 Database Setup

* PostgreSQL connected to backend
* SQLAlchemy configured
* Alembic migrations initialized
* Models created:

  * Users
  * Projects
  * Scan Runs
* Initial migration generated and applied

## Day 3 Authentication System

* User registration endpoint (`POST /auth/register`)
* User login endpoint (`POST /auth/login`)
* Password hashing using bcrypt
* JWT token generation
* Protected route implemented
* Current user endpoint (`GET /auth/me`)

## Run the project

```bash
docker compose up --build
```

## URLs

* Frontend: http://localhost:3000
* Backend: http://localhost:8000
* API Docs: http://localhost:8000/docs
* Health check: http://localhost:8000/health

## Test Authentication

### Register

POST `/auth/register`

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```

### Login

POST `/auth/login`

Response:

```json
{
  "access_token": "your_token_here",
  "token_type": "bearer"
}
```

### Get Current User

GET `/auth/me`

Header:

```
Authorization: Bearer <your_token>
```

## Current Status

* Backend working with authentication
* Database connected with migrations
* Docker setup running all services

## Next Steps

* Frontend authentication (login/register UI)
* Dashboard implementation
* File upload and analysis features
