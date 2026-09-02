# Hello Project

A demonstration project combining:

1. **DTE Demo** — A minimal Python module (`src/hello.py`) with formal requirements specification and CI/CD evidence generation, used as an example for Development, Test & Evaluation documentation
2. **Fullstack Example** — A modern web application with a FastAPI backend and React frontend that wraps the greeting logic into a production-like architecture

## What it does

**DTE Demo:** A simple greeting function with comprehensive documentation and testing framework.

**Fullstack App:**
- **Frontend**: A React (Vite + TypeScript) form where users enter their name  
- **Backend**: A FastAPI REST API that generates and validates personalized greetings
- **Communication**: HTTP POST request/response flow with CORS support

Enter your name in the frontend, submit the form, and receive a personalized greeting from the backend API. The app demonstrates modern fullstack patterns: API design, input validation, error handling, and async request flow.

## Architecture

```
┌─────────────────┐
│  React Frontend │
│  (Vite + TS)    │
└────────┬────────┘
         │ POST /api/greet
         │ { "name": "Alice" }
         │
         ▼
┌─────────────────────┐
│  FastAPI Backend    │
│                     │
│ • Validates input   │
│ • Generates greet   │
│ • Returns JSON      │
└─────────────────────┘
```

## Prerequisites

- **Python 3.11+** (for the backend)
- **Node.js 18+** (for the frontend)
- **npm** (frontend package manager)

## Setup and Running

### Backend

Install dependencies:
```bash
cd backend
pip install -r requirements.txt
# or if venv doesn't work in your environment:
# pip install --target .pylibs -r requirements.txt
# export PYTHONPATH=.pylibs
```

Run the development server:
```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

### Frontend

Install dependencies and start the dev server:
```bash
cd frontend
npm install
npm run dev
```

The frontend will typically run on `http://localhost:5173`.

Open that URL in your browser, enter a name, and submit the form to test the greeting flow.

## Running Tests

### DTE Demo (original module)

```bash
pip install pytest
pytest tests/test_hello.py -v
```

4 tests verify the original requirements (REQ-001 through REQ-004).

### Backend (fullstack API)

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

All 7 tests should pass:
- 4 unit tests for the greeting logic (matching DTE requirements)
- 3 API integration tests for the FastAPI endpoints

### Frontend (fullstack UI)

TypeScript type-checking (via build):
```bash
cd frontend
npm install
npm run build  # TypeScript will error if there are type errors
```

## API Reference

### POST /api/greet

Generate a greeting for the given name.

**Request:**
```json
{
  "name": "Alice"
}
```

**Response (200 OK):**
```json
{
  "greeting": "Hello, Alice!"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Name cannot be empty"
}
```

### GET /health

Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

## Project Structure

```
hello-project/
├── README.md
├── .gitignore
│
├── DTE Demo (original requirements-based module):
├── src/
│   ├── __init__.py
│   └── hello.py                Original greeting module
├── tests/
│   ├── __init__.py
│   └── test_hello.py           Unit tests matching requirements
├── docs/
│   ├── requirements.md         Software Requirements Specification (REQ-001 through REQ-005)
│   └── design.md               Software Design Document (SCI-001)
├── pytest.ini
│
├── Fullstack Example (modern web application):
├── backend/
│   ├── requirements.txt        FastAPI, uvicorn, pytest, etc.
│   ├── pytest.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             FastAPI application with /api/greet endpoint
│   │   └── greeting.py         Greeting logic (uses src.hello internally)
│   └── tests/
│       ├── __init__.py
│       ├── test_greeting.py    Unit tests for greeting module
│       └── test_main.py        API integration tests
│
├── frontend/
│   ├── package.json            React + Vite + TypeScript dependencies
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── .gitignore
│   └── src/
│       ├── main.tsx            React entry point
│       ├── App.tsx             Main UI component (form + greeting display)
│       ├── App.css             Styled components
│       └── api.ts              Typed API client for backend
│
└── .github/
    └── workflows/
        └── ci.yml              GitHub Actions CI (backend tests + frontend build)
```

## How the DTE Demo and Fullstack App Work Together

The **DTE Demo** (`src/hello.py`, `tests/test_hello.py`, `docs/`) is the original core module that implements the greeting requirements.

The **Fullstack Example** wraps this core logic:
- The backend (`backend/app/greeting.py`) imports and uses the original `hello()` function from `src/hello.py`
- The backend API exposes this as a REST endpoint
- The frontend calls the backend API via HTTP
- The same unit tests verify the greeting logic works both in the original and backend context

This design demonstrates how a simple library can be exposed through a modern web API and consumed by a frontend application.

## Development Notes

- The backend runs on port 8000 by default
- The frontend (Vite dev server) runs on port 5173 by default
- CORS is configured to allow requests from both localhost:5173 and localhost:3000
- The greeting validation happens in the backend; empty names return a 400 error
- The DTE demo documentation is in `docs/requirements.md` and `docs/design.md`

## Technology Stack

**Backend:**
- FastAPI — modern Python web framework
- Uvicorn — ASGI server
- Pydantic — data validation
- Pytest — testing framework

**Frontend:**
- React 18 — UI library
- Vite — build tool and dev server
- TypeScript — type-safe JavaScript
