# DevLens

DevLens is an AI-powered web application that helps developers understand, analyze, and improve codebases.

---

## 🚀 Tech Stack

* **Frontend:** Next.js + TypeScript + Tailwind CSS
* **Backend:** FastAPI + Python
* **Database:** PostgreSQL
* **ORM & Migrations:** SQLAlchemy + Alembic
* **Auth:** JWT (JSON Web Tokens)
* **Containers:** Docker + Docker Compose

---

## 📦 Features Implemented (Day 1–3)

### ✅ Day 1 – Project Setup

* Next.js frontend initialized
* FastAPI backend initialized
* PostgreSQL with Docker
* Docker Compose setup
* Environment variables configured
* `/health` endpoint working

### ✅ Day 2 – Database Foundation

* SQLAlchemy configured
* PostgreSQL connected to backend
* Alembic migrations setup
* Models created:

  * Users
  * Projects
  * Scan Runs
* Initial migration generated and applied

### ✅ Day 3 – Authentication System

* User registration (`POST /auth/register`)
* User login (`POST /auth/login`)
* Password hashing with bcrypt
* JWT token generation
* Protected routes implemented
* Get current user (`GET /auth/me`)

---

## 🛠️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/devlens.git
cd devlens
```

### 2. Start all services

```bash
docker compose up --build
```

---

## 🌐 Available Services

* Frontend → http://localhost:3000
* Backend → http://localhost:8000
* API Docs (Swagger) → http://localhost:8000/docs
* Health Check → http://localhost:8000/health

---

## 🧪 Testing Authentication

### Register

`POST /auth/register`

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```

### Login

`POST /auth/login`

Returns:

```json
{
  "access_token": "your_token_here",
  "token_type": "bearer"
}
```

### Protected Route

`GET /auth/me`

Header:

```
Authorization: Bearer <your_token>
```

---

## 📁 Project Structure

```
devlens/
  backend/
    app/
      api/routes/
      core/
      models/
      schemas/
      services/
      main.py
    alembic/
  frontend/
    app/
    public/
  docker-compose.yml
  README.md
```

---

## 📌 Current Status

✔ Backend fully functional with authentication
✔ Database connected with migrations
✔ Dockerized development environment

---

## 🔜 Next Steps

* Day 4: Frontend authentication (login/register UI)
* Dashboard UI
* File upload + code analysis pipeline

---

## 🧠 Vision

DevLens aims to become an AI-powered developer tool that:

* Analyzes codebases
* Detects issues and inefficiencies
* Provides actionable insights

---

## 📜 License

This project is for learning and development purposes.
