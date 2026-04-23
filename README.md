# DevLens

DevLens is an AI-powered web application that helps developers understand and improve codebases.

## Tech Stack

* Frontend: Next.js + TypeScript + Tailwind CSS
* Backend: FastAPI + Python
* Database: PostgreSQL
* Containers: Docker + Docker Compose

## Day 1 Setup Complete

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

## Day 4 Frontend Authentication

* Login page implemented
* Register page implemented
* Form validation added (client-side)
* API integration with backend authentication
* Token storage implemented
* Redirect after login working
* Redirect guard for authenticated users (prevent access to login/register)

## Run the project

```bash
docker compose up --build
```

## Running servers

### Frontend
Home:

```
http://localhost:3000/
```

Dashboard:
```
http://localhost:3000/dashboard
```

Login Page:
```
http://localhost:3000/login
```

Register Page:
```
http://localhost:3000/register
```

---

### Backend

Base URL:
```
http://localhost:8000/
```

Health Check:
```
http://localhost:8000/health
```

API Docs (Swagger):
```
http://localhost:8000/docs
```

---

### Auth Endpoints

Register:
```
POST http://localhost:8000/auth/register
```

Login:
```
POST http://localhost:8000/auth/login
```

Get Current User:
```
GET http://localhost:8000/auth/me
```
