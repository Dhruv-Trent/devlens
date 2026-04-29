# DevLens

DevLens is an AI-powered web application that helps developers understand and improve codebases.

## Tech Stack

* Frontend: Next.js + TypeScript + Tailwind CSS
* Backend: FastAPI + Python
* Database: PostgreSQL
* Containers: Docker + Docker Compose

---

## Day 1 Setup Complete

* Frontend initialized
* Backend initialized
* PostgreSQL added
* Docker Compose added
* Health check endpoint working

---

## Day 2 Database Setup

* PostgreSQL connected to backend
* SQLAlchemy configured
* Alembic migrations initialized
* Models created:

  * Users
  * Projects
  * Scan Runs
* Initial migration generated and applied

---

## Day 3 Authentication System

* User registration endpoint (`POST /auth/register`)
* User login endpoint (`POST /auth/login`)
* Password hashing using bcrypt
* JWT token generation
* Protected route implemented
* Current user endpoint (`GET /auth/me`)

---

## Day 4 Frontend Authentication

* Login page implemented
* Register page implemented
* Form validation added (client-side)
* API integration with backend authentication
* Token storage implemented
* Redirect after login working
* Redirect guard for authenticated users

---

## Day 5 Project Management

* Project creation endpoint (`POST /projects`)
* Get all user projects (`GET /projects`)
* Get single project (`GET /projects/{project_id}`)
* Project ownership validation implemented
* Database relationship between users and projects established
* Frontend dashboard created
* Project list displayed on dashboard
* Create project UI implemented
* Navigation between dashboard and project detail page

---

## Day 6 Repository Upload System

* Upload repository endpoint (`POST /projects/{project_id}/upload`)
* `.zip` file validation implemented
* File size limit enforced (50 MB)
* Uploaded files stored on disk (`backend/uploads`)
* Scan run record created in database
* Upload tied to project ownership (auth protected)
* Frontend upload component implemented
* Upload UI added to project detail page
* Success and error handling in UI
* Invalid file types rejected (frontend + backend validation)

---

## Day 7 Repository Extraction & Scan Orchestration

* Background scan process implemented using FastAPI BackgroundTasks
* Scan lifecycle implemented:

  * `pending → processing → completed / failed`
* Safe `.zip` extraction implemented (prevents path traversal attacks)
* Extracted repositories stored in:

  * `backend/extracted_repos/`
* Existing extracted folders cleaned before re-scan
* Ignored folders during scan:

  * `.git`, `node_modules`, `.next`, `dist`, `build`, `venv`, `__pycache__`, etc.
* Recursive repository traversal implemented
* Total file count calculation added
* Scan metadata updated in database:

  * `extracted_path`
  * `total_files`
  * `started_at`
  * `completed_at`
  * `error_message`
* Error handling added for corrupted or invalid zip files
* Scan endpoints implemented:

  * `GET /projects/{project_id}/scans`
  * `GET /scans/{scan_id}`
* Optional frontend scan list component added
* Upload now automatically triggers scan process

---

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
