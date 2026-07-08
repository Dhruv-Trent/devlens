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

## Day 8 File Metadata Storage & Repository Tree

* File model created and connected to projects + scan runs
* `files` table added through Alembic migration
* Repository file metadata stored in database after scan
* Supported file type detection implemented
* Language inference added from file extensions
* File metadata stored:

  * `path`
  * `filename`
  * `extension`
  * `language`
  * `size_bytes`
  * `content_preview`
  * `is_supported`
* Unsupported files skipped or marked
* Repository file previews saved for supported files
* File processing integrated into scan pipeline
* Recursive repository tree builder implemented
* Tree sorting implemented (folders first, files second)
* File tree API endpoint implemented:

  * `GET /projects/{project_id}/files/tree`
* Frontend repository tree component created
* Expand/collapse folder UI implemented
* Repository tree integrated into project detail page
* Clickable file nodes added for future file viewer support
* Cross-platform path normalization added (`/` separator handling)
* Supported file counts now tracked per scan

---

## Day 9 File Viewer & File Detail API

* File detail API endpoint implemented:

  * `GET /files/{file_id}`
* File ownership validation added for secure file access
* File detail loading connected to frontend
* File viewer component created
* Repository tree file selection implemented
* Selected file highlighting added in repository tree
* File viewer displays:

  * filename
  * full file path
  * detected language
  * extension
  * file size
  * supported file status
* Safe code/content preview rendering implemented
* Summary placeholder added for future AI summaries
* Two-column project workspace layout added:

  * repository tree
  * file viewer panel
* Loading and empty states implemented for file viewer
* Cross-user file access protection verified
* Repository browsing workflow improved for uploaded scans

---

## Day 10 File Chunking System

* `FileChunk` model created
* `file_chunks` table added through Alembic migration
* Chunking service implemented
* Supported files automatically split into chunks after scan
* Chunk overlap strategy implemented for better future retrieval quality
* Line-aware chunk splitting added to preserve cleaner code boundaries
* Chunk metadata stored:

  * `file_id`
  * `chunk_index`
  * `content`
  * `token_count_estimate`
* Chunk ordering preserved for reconstruction and retrieval
* Automatic chunk generation integrated into scan pipeline
* Existing chunks cleared before re-processing scans
* `chunk_count` tracking added to scan runs
* Chunk estimation logic added for future embedding support
* File chunk API endpoint implemented:

  * `GET /files/{file_id}/chunks`
* Database verification and chunk retrieval testing completed
* Foundation prepared for Day 11 embeddings integration

---

## Day 11 Embedding Infrastructure & Vector Search Foundation

* pgvector database extension enabled
* Vector support added to PostgreSQL
* Embedding column added to file chunks
* Embedding service implemented
* OpenAI embedding integration configured
* Vector search service implemented
* Semantic chunk search endpoint added:

  * `GET /projects/{project_id}/search-chunks`
* Chunk similarity retrieval logic implemented
* Scan pipeline integrated with embedding generation
* Embedding failures no longer break repository scans
* Search endpoint gracefully handles missing embeddings
* Scan rollback and error recovery improved
* File preview sanitization added for NUL-byte safety
* Foundation prepared for semantic code search
* Ready for future migration to local embedding models

---

## Day 12 AI File Summaries

* Summary generation service implemented
* File summaries stored in database
* Summary generation integrated into scan pipeline
* File viewer updated to display summaries
* Summary persistence added through `files.summary`
* Scan process continues even if summary generation fails
* Error handling added for AI service failures
* Summary panel integrated into DevLens workspace
* Foundation prepared for AI-powered code understanding
* Ready for future migration to local LLM summarization

---

## Day 13 Automated Findings Engine

* Issues model created
* `issues` table added through Alembic migration
* Issue schema implemented
* Findings generation service created
* Automated repository analysis added during scan process
* TODO/FIXME/HACK/XXX comment detection implemented
* Hardcoded secret detection implemented

  * API_KEY
  * SECRET
  * PASSWORD
  * TOKEN
  * Private key markers
* Risky code pattern detection implemented

  * eval()
  * exec()
  * pickle.loads
  * innerHTML usage
* Large file detection implemented

  * Low severity: 300+ lines
  * Medium severity: 500+ lines
  * High severity: 800+ lines
* Missing test detection implemented
* Issue severity levels added

  * low
  * medium
  * high
* Findings linked to:

  * Project
  * Scan Run
  * File
* Scan pipeline updated to generate findings automatically after summaries
* Findings count tracked per scan
* Findings API endpoint implemented

  * `GET /projects/{project_id}/issues`
* Project ownership validation added to findings endpoint
* Latest completed scan findings retrieval implemented
* Frontend issue type created
* Findings panel component created
* Findings API integration added
* Severity badge UI implemented
* Issue suggestions displayed in frontend
* Line references displayed for findings
* Findings integrated into project detail page
* End-to-end testing completed using sample repositories

---

## Day 14 Repository Chat Backend

* Chat message model created
* `chat_messages` table added through Alembic migration
* Chat schemas implemented
* Chat service created
* Chat history persistence added
* User and assistant messages stored in database
* Latest completed scan detection implemented
* Repository question-answering backend created
* Retrieval connection added using file chunks and vector search
* Chat endpoint implemented:

  * `POST /projects/{project_id}/chat`
* Chat history endpoint implemented:

  * `GET /projects/{project_id}/chat`
* Project ownership validation added to chat endpoints
* Empty message validation added
* Chat backend safely handles unavailable embeddings or API quota errors
* Chat responses saved even when retrieval is unavailable
* Foundation prepared for full repository Q&A and Day 15 chat UI

---

## Day 15 Repository Chat UI

* Frontend chat message types created
* Chat panel component implemented
* Chat history loading added
* User and assistant messages displayed in UI
* Chat input form added
* Send button and submit handling implemented
* Starter prompts added:

  * What does this project do?
  * Where is authentication handled?
  * Which files seem most important?
  * What should I refactor first?
* Loading state added while assistant response is pending
* Error state added for failed chat requests
* Auto-scroll behavior added for new messages
* Chat panel integrated into project detail page
* Backend chat history connected to frontend
* Messages persist after page refresh
* UI gracefully displays backend fallback responses when embeddings/API quota are unavailable

---

## Day 16 Project Overview & Scan History

* Project overview component created
* Latest completed scan summary displayed
* Repository health snapshot added
* Overview metrics displayed:

  * Total Files
  * Supported Files
  * Chunks
  * Findings
* Latest scan status badge implemented
* Scan history component refactored to accept scan data as props
* Project page now loads scan history from backend
* Scan loading state implemented
* Latest scan automatically derived from scan history
* Refresh scans button added
* Manual scan history refresh implemented
* Repository upload component updated with upload completion callback
* Upload automatically refreshes scan history after successful scan
* Project overview automatically updates after new scans
* Scan history displays:

  * Scan ID
  * Created time
  * Started time
  * Completed time
  * Total files
  * Supported files
  * Chunk count
  * Findings count
  * Scan status
* Frontend state management improved for project dashboard
* Project workspace layout reorganized:

  * Project Overview
  * Upload Repository
  * Scan History
  * Findings
  * Repository Tree
  * File Viewer
  * AI Repository Assistant
* End-to-end testing completed for scan refresh workflow
* Chat integration verified after project page refactor
* Foundation prepared for richer project analytics and future dashboard enhancements

---
## Day 17 Additional Improvements

- Prevented automatic page scrolling to the AI Assistant when opening a project.
- Chat now automatically scrolls only when the user sends or receives new messages.
- Improved overall chat user experience by avoiding unwanted scrolling during chat history loading.

---

## Day 18 Testing & Bug Fixing

* Created a comprehensive `TESTING.md` checklist
* Performed a fresh full application startup test

### Authentication Testing

* Verified user registration
* Verified duplicate registration handling
* Verified user login
* Verified invalid login handling
* Verified logout functionality
* Verified protected route access

### Project Management Testing

* Verified project creation
* Verified dashboard project listing
* Verified project detail page
* Verified project persistence after page refresh

### Repository Upload & Scan Testing

* Verified successful ZIP repository upload
* Verified scan creation
* Verified scan completion
* Verified project overview updates after scan
* Verified scan history updates correctly

### Upload Validation Testing

* Verified non-ZIP file rejection
* Verified corrupt ZIP failure handling
* Verified failed scan status updates
* Verified appropriate error messages for invalid uploads

### Repository Explorer Testing

* Verified repository tree loading
* Verified file selection
* Verified file viewer updates
* Verified content preview rendering

### Findings System Testing

* Verified findings generation
* Verified severity badge rendering
* Verified issue suggestions
* Verified findings persistence after page refresh

### AI Repository Assistant Testing

* Verified chat history loading
* Verified starter prompts
* Verified message sending
* Verified loading state
* Verified assistant responses
* Verified chat history persistence

### Chat UX Improvements

* Prevented automatic page scrolling during initial chat history load
* Enabled automatic scrolling only when new messages are sent or received

### Security & Authorization Testing

* Verified users cannot access other users' projects
* Verified protected API endpoints return appropriate authorization responses

### Backend Verification

* Verified backend health endpoint
* Verified Swagger API documentation

### Final Validation

* Confirmed all major frontend workflows function correctly after application restart

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
