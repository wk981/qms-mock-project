# Hello App — A Fullstack Example

A minimal fullstack application demonstrating a **FastAPI backend** and **React frontend** that work together to provide a simple greeting service.

## What it does

- **Frontend**: A React form where users enter their name
- **Backend**: A FastAPI service that generates personalized greetings
- **Communication**: REST API over HTTP

Enter your name, submit the form, and receive a personalized greeting. The app demonstrates basic request/response handling, input validation, and error display.

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

### Backend tests

```bash
cd backend
# If using .pylibs:
PYTHONPATH=.pylibs python3 -m pytest tests/

# Or if installed normally:
pytest tests/
```

All 7 tests should pass:
- 4 unit tests for the greeting logic
- 2 API tests for the FastAPI endpoints
- 1 health check test

### Frontend tests

TypeScript type-checking (via build):
```bash
cd frontend
npm run build  # TypeScript will fail the build if there are type errors
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
├── backend/
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             FastAPI application
│   │   └── greeting.py         Greeting logic
│   └── tests/
│       ├── __init__.py
│       ├── test_greeting.py    Unit tests
│       └── test_main.py        API tests
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── .gitignore
│   └── src/
│       ├── main.tsx
│       ├── App.tsx             Main React component
│       ├── App.css
│       └── api.ts              API client
└── .github/
    └── workflows/
        └── ci.yml              GitHub Actions CI
```

## Development Notes

- The backend runs on port 8000 by default
- The frontend (Vite dev server) runs on port 5173 by default
- CORS is configured to allow requests from both localhost:5173 and localhost:3000
- The greeting validation happens on the backend; empty names return a 400 error

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
