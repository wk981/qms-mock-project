# Software Design Document

| Field | Value |
|---|---|
| Project | Hello Project |
| Repository | `hello-project` |
| Version | 2.0.0 |
| Related document | [Software Requirements Specification](requirements.md) |

## 1. Architecture

The application is a fullstack web service with three layers:

1. **Frontend** — A web-based user interface (React + TypeScript) running in the browser
2. **Backend** — A REST API service (FastAPI + Python) exposing the greeting operation over HTTP
3. **Core Logic** — A pure Python module that implements the greeting functionality

Data flow:

```text
User (Browser)
  │
  ├─► frontend/src/App.tsx  (React UI, form submission)
  │       │
  │       ▼
  │   frontend/src/api.ts   (HTTP client)
  │       │
  │       │  HTTP POST /api/greet
  │       │
  ▼       ▼
backend/app/main.py  (FastAPI)
  │
  ├─► request validation (Pydantic)
  │
  ├─► backend/app/greeting.py  (greeting wrapper)
  │
  ▼
src/hello.py  ──►  hello(name)  ──►  greeting string
                        │
                        └───────►  ValueError (invalid input)
```

Each layer is responsible for a distinct concern:
- The **core module** (`src/hello.py`) validates input and generates greetings
- The **backend** (`backend/app/main.py`) translates HTTP requests to Python function calls
  and HTTP responses, enforcing API contracts via Pydantic models
- The **frontend** (`frontend/src/App.tsx`) provides a user-friendly form interface and
  handles async request/response flow

## 2. Software Configuration Items

### SCI-001 — Core Greeting Module

Location: `src/hello.py`

This module is responsible for:

* **generating greetings** — constructing the greeting text from the supplied name
* **validating input** — rejecting an empty name before a greeting is constructed

| Attribute | Value |
|---|---|
| Configuration item | SCI-001 |
| File | `src/hello.py` |
| Language | Python 3 |
| Safety classification | Safety-critical |
| Requirements allocated | REQ-001, REQ-002, REQ-003, REQ-004 |
| Unit tests | `tests/test_hello.py`, `backend/tests/test_greeting.py` |

### SCI-002 — FastAPI Application

Location: `backend/app/main.py`

This module is responsible for:

* **HTTP routing** — accepting POST requests to `/api/greet`
* **request validation** — parsing and validating JSON request bodies using Pydantic models
* **response formatting** — returning JSON responses with greeting or error messages
* **error handling** — translating Python exceptions (ValueError from the core module) into
  appropriate HTTP status codes and error detail messages

| Attribute | Value |
|---|---|
| Configuration item | SCI-002 |
| File | `backend/app/main.py` |
| Language | Python 3 |
| Requirements allocated | REQ-006, REQ-007 |
| Integration tests | `backend/tests/test_main.py` |
| Dependencies | FastAPI, Pydantic, SCI-001 |

### SCI-003 — React Frontend Application

Location: `frontend/src/App.tsx`

This component is responsible for:

* **user input collection** — a form input field for the user's name
* **API communication** — sending POST requests to `/api/greet` via `frontend/src/api.ts`
* **response handling** — displaying the greeting or error message returned from the backend
* **user feedback** — loading states, form submission handling, and error display

| Attribute | Value |
|---|---|
| Configuration item | SCI-003 |
| File | `frontend/src/App.tsx` |
| Language | TypeScript / React |
| Requirements allocated | REQ-008 |
| Test coverage | Manual exploratory testing (no automated tests) |
| Dependencies | React, SCI-002 (via HTTP) |

## 3. Core Module Interface (SCI-001)

```text
hello(name: str) -> str
```

**Input**

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | The name to greet. Must be a non-empty string. |

**Output**

A greeting string of the form `Hello, <name>!`.

**Error Handling**

An empty name raises `ValueError("Name cannot be empty")`. The validation check is
performed before greeting construction.

**Example**

```text
hello("Alice")  →  "Hello, Alice!"
hello("")       →  ValueError: Name cannot be empty
```

## 4. REST API Interface (SCI-002)

### POST /api/greet

**Request**

```json
{
  "name": "string"
}
```

**Response (200 OK)**

```json
{
  "greeting": "Hello, Alice!"
}
```

**Response (400 Bad Request)**

```json
{
  "detail": "Name cannot be empty"
}
```

**Behavior**

- Accepts JSON POST request with a `name` field
- Calls the core module's `hello(name)` function
- Returns the greeting in a JSON response object
- Translates `ValueError` exceptions to HTTP 400 with the error message as `detail`

## 5. Frontend Interface (SCI-003)

The React component provides:

- A text input field labeled "Enter your name"
- A "Get Greeting" button to submit the form
- A result area displaying either the greeting (green background) or an error message (red background)
- Loading state feedback during API request
- Form clearing on successful submission

## 6. Error Handling

**Core Module (SCI-001)**
- Empty input raises `ValueError` before processing

**API Layer (SCI-002)**
- Catches `ValueError` and translates to HTTP 400 with error detail
- Pydantic validation errors are implicitly handled by the framework

**Frontend (SCI-003)**
- Displays backend error detail messages to the user
- Shows loading state during request
- Allows retrying after an error

## 7. Design Limitations

- **REQ-005 (Logging)** is not implemented. Neither the core module nor the backend API
  generates structured log entries for greeting requests. This is a known gap.

- **Frontend testing** — SCI-003 has no automated test suite. Requirement REQ-008
  is verified by manual exploratory testing only.

- **Data persistence** — The system does not store greeting history or any state
  across requests. Each request is independent.
