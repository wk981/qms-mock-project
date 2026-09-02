# Software Design Document

**Status:** DRAFT  
**Project:** Hello Project  
**Generated:** 2026-09-02  
**Related Document:** [Software Requirements Specification](software-requirements-specification.md)  

## 1. Purpose

This document describes the detailed software design and implementation of the Hello Project based on verified requirements and observed source code. It documents the software architecture, components, modules, interfaces, and design decisions that implement the system requirements.

## 2. Software Scope

This document covers the complete software design of the Hello Project:
- Core greeting module (SCI-001)
- Backend REST API (SCI-002)
- Frontend web UI (SCI-003)

Out of scope:
- Deployment infrastructure and containerization
- Production environment configuration
- Performance tuning or optimization

## 3. Software Architecture

### 3.1 Architectural Style

**Type:** Layered (3-tier) architecture with clear separation of concerns  
**Evidence:** `docs/design.md` section 1, observed source code structure  

```
┌───────────────────────────────────────────────────┐
│         Client Layer (Browser)                    │
│  Frontend SPA: React/TypeScript/Vite              │
│  frontend/src/App.tsx, api.ts                     │
└──────────────────┬────────────────────────────────┘
                   │ HTTP(S)
                   │ POST /api/greet
                   ▼
┌───────────────────────────────────────────────────┐
│         Application Layer (Server)                │
│  REST API: FastAPI/Pydantic/Uvicorn              │
│  backend/app/main.py                             │
│  • HTTP routing                                   │
│  • Request/response validation                    │
│  • Error translation                              │
└──────────────────┬────────────────────────────────┘
                   │ Function call
                   │ hello(name)
                   ▼
┌───────────────────────────────────────────────────┐
│         Business Logic Layer                      │
│  Core Module: Pure Python                         │
│  src/hello.py                                     │
│  • Input validation                               │
│  • Greeting generation                            │
└───────────────────────────────────────────────────┘
```

### 3.2 Architectural Principles

1. **Single Responsibility** — Each layer has one clear concern
2. **Dependency Direction** — Upper layers depend on lower layers; lower layers are independent
3. **Fail-Safe Defaults** — Input validation at multiple layers (defense in depth)
4. **Typed Interfaces** — Type annotations and Pydantic models enforce contracts

**Evidence:** Consistent across all three source directories; no circular dependencies observed

## 4. Software Configuration Items

### 4.1 SCI-001: Core Greeting Module

**Location:** `src/hello.py`  
**Language:** Python 3.11+  
**Type:** Pure Python module (no external dependencies)  
**Classification:** EVIDENCE — observed implementation  

#### 4.1.1 Module Contents

| Item | Type | LOC | Purpose |
|---|---|---|---|
| `DEFAULT_GREETING` | Constant | 1 | Default greeting prefix ("Hello") |
| `hello(name: str) -> str` | Function | 13 | Core greeting generation function |

#### 4.1.2 Implementation

**Source:** `src/hello.py:1-31`  

```python
def hello(name: str) -> str:
    if not name:
        raise ValueError("Name cannot be empty")
    return f"{DEFAULT_GREETING}, {name}!"
```

**Logic Flow:**
1. Accept `name` parameter (string)
2. Validate: if name is falsy (empty, None), raise `ValueError`
3. Generate greeting using f-string: "Hello, {name}!"
4. Return greeting string

#### 4.1.3 Error Handling

- **Input Error:** Empty name → `ValueError("Name cannot be empty")`
- **Error Semantics:** Exception raised *before* formatting; prevents construction of invalid greetings

#### 4.1.4 Dependencies

- Python standard library only (no external packages)
- No I/O, network, or filesystem access

#### 4.1.5 Tests

| Test | File | Line | Requirement |
|---|---|---|---|
| `test_greeting_contains_name()` | `tests/test_hello.py:11-13` | Asserts name in result | REQ-001 |
| `test_default_greeting()` | `tests/test_hello.py:16-18` | Asserts "Hello" prefix | REQ-002 |
| `test_empty_name_is_rejected()` | `tests/test_hello.py:21-24` | Asserts ValueError raised | REQ-003 |
| `test_greeting_ends_with_exclamation_mark()` | `tests/test_hello.py:27-29` | Asserts "!" suffix | REQ-004 |

**Evidence:** 4 tests, all pass. Executed in CI pipeline on every commit.

### 4.2 SCI-002: FastAPI Backend Application

**Location:** `backend/app/`  
**Language:** Python 3.11  
**Framework:** FastAPI 0.24.x, Pydantic 2.x, Uvicorn 0.24.x  
**Type:** HTTP REST API server  
**Classification:** EVIDENCE — observed implementation  

#### 4.2.1 Module Structure

| Module | File | Purpose |
|---|---|---|
| `greeting` | `backend/app/greeting.py` | Greeting logic wrapper |
| `main` | `backend/app/main.py` | FastAPI application, endpoints, middleware |

#### 4.2.2 Data Models (Pydantic)

**Source:** `backend/app/main.py:10-15`  

```python
class GreetRequest(BaseModel):
    name: str

class GreetResponse(BaseModel):
    greeting: str
```

**Validation:**
- `GreetRequest.name` is required string; Pydantic validates JSON parsing
- `GreetResponse.greeting` is required string; ensures response shape

#### 4.2.3 HTTP Endpoints

**POST /api/greet**

| Component | Value |
|---|---|
| Method | POST |
| Path | `/api/greet` |
| Request Body | JSON: `{"name": "string"}` |
| Response (200) | JSON: `{"greeting": "string"}` |
| Response (400) | JSON: `{"detail": "error message"}` |
| Handler | `greet()` function in `backend/app/main.py:29-36` |

**Implementation:**

```python
@app.post("/api/greet", response_model=GreetResponse)
def greet(request: GreetRequest) -> GreetResponse:
    try:
        greeting_text = hello(request.name)
        return GreetResponse(greeting=greeting_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**Logic Flow:**
1. Receive and parse JSON request (Pydantic validates)
2. Call `hello(request.name)` from `app.greeting` module
3. Wrap result in `GreetResponse` model
4. Catch `ValueError` and translate to HTTP 400 with detail message

**GET /health**

| Component | Value |
|---|---|
| Method | GET |
| Path | `/health` |
| Response (200) | JSON: `{"status": "ok"}` |
| Handler | `health_check()` function in `backend/app/main.py:39-42` |

#### 4.2.4 Middleware and Configuration

**CORS Middleware**

**Source:** `backend/app/main.py:20-26`  

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Purpose:** Allow cross-origin requests from frontend dev servers  
**Origins:** Hardcoded to localhost (development only)  
**Classification:** EVIDENCE + FINDING — Production deployment must reconfigure

#### 4.2.5 Dependencies

| Dependency | Version | Purpose |
|---|---|---|
| FastAPI | 0.24.x | HTTP framework |
| Pydantic | 2.x | Request/response validation |
| Uvicorn | 0.24.x | ASGI server |
| src.hello | (local) | Core greeting logic |

**Evidence:** `backend/requirements.txt`

#### 4.2.6 Tests

| Test | File | Line | Requirement |
|---|---|---|---|
| `test_greet_success()` | `backend/tests/test_main.py:12-20` | POST /api/greet success case | REQ-006 |
| `test_greet_empty_name()` | `backend/tests/test_main.py:23-28` | POST /api/greet 400 error | REQ-007 |
| `test_health_check()` | `backend/tests/test_main.py:31-35` | GET /health endpoint | REQ-006 |

**Evidence:** 3 tests, all pass. Executed in CI pipeline.

### 4.3 SCI-003: React Frontend Application

**Location:** `frontend/src/`  
**Language:** TypeScript + JSX (React 18)  
**Build Tool:** Vite  
**Type:** Single-Page Application (SPA)  
**Classification:** EVIDENCE — observed implementation  

#### 4.3.1 Component Structure

| Component | File | Purpose |
|---|---|---|
| `App` | `frontend/src/App.tsx` | Main UI component (form, state, result display) |
| API client | `frontend/src/api.ts` | Typed HTTP client for backend |

#### 4.3.2 Main Component: App

**Source:** `frontend/src/App.tsx`  

**State Management:**

```typescript
const [name, setName] = useState('')
const [greeting, setGreeting] = useState<string | null>(null)
const [error, setError] = useState<string | null>(null)
const [loading, setLoading] = useState(false)
```

**State Semantics:**
- `name` — user input (controlled input)
- `greeting` — result greeting (null if no result)
- `error` — error message (null if no error)
- `loading` — request in progress

**UI Elements:**

| Element | Purpose | Code Reference |
|---|---|---|
| Form | User input submission | `App.tsx:32-44` |
| Text input | Name entry | `App.tsx:33-40` |
| Submit button | Trigger greeting | `App.tsx:41-43` |
| Success result | Display greeting | `App.tsx:46-49` |
| Error result | Display error message | `App.tsx:52-55` |

**Event Handlers:**

```typescript
async function handleSubmit(e: React.FormEvent) {
  e.preventDefault()
  setError(null)
  setGreeting(null)
  setLoading(true)
  
  try {
    const response = await greet(name)
    setGreeting(response.greeting)
    setName('')
  } catch (err) {
    setError(err instanceof Error ? err.message : 'An error occurred')
  } finally {
    setLoading(false)
  }
}
```

**Logic Flow:**
1. User enters name in input field
2. User clicks "Get Greeting" button (or submits form)
3. Clear previous result/error
4. Set loading state, disable form
5. Call `greet(name)` API function
6. On success: display greeting, clear input, enable form
7. On error: display error message, enable form
8. Finally: clear loading state

#### 4.3.3 API Client Module

**Source:** `frontend/src/api.ts`  

**Interfaces:**

```typescript
interface GreetRequest {
  name: string
}

interface GreetResponse {
  greeting: string
}

async function greet(name: string): Promise<GreetResponse>
```

**HTTP Implementation:**

```typescript
const response = await fetch(`${API_BASE_URL}/api/greet`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name } as GreetRequest),
})

if (!response.ok) {
  const error = await response.json()
  throw new Error(error.detail || 'Failed to get greeting')
}

return response.json()
```

**Error Handling:**
- If HTTP response is not 2xx, parse error JSON and throw with detail message
- Caller (App component) catches and displays error

#### 4.3.4 Styling

**File:** `frontend/src/App.css`  
**Purpose:** Visual presentation (form styling, result colors, loading state)  
**Type:** Plain CSS  

#### 4.3.5 Dependencies

| Dependency | Purpose |
|---|---|
| React 18 | UI framework |
| TypeScript | Type checking |
| Vite | Build tool, dev server |

**Evidence:** `frontend/package.json`

#### 4.3.6 Tests

**Current Status:** Manual exploratory testing only  
**Classification:** EVIDENCE + FINDING — No automated tests present  

**Manual Test Cases (observed):**
1. Enter valid name, submit → greeting displayed
2. Leave input empty, submit → error displayed
3. Submit form, observe loading state → button shows "Loading..."
4. After success, input field cleared
5. Can submit another greeting after error

**Verification Method:** Manual testing (as documented in `docs/requirements.md`)

## 5. Interfaces

### 5.1 Core Module Interface (SCI-001)

**Function Signature:**

```python
def hello(name: str) -> str
```

**Input:**
- `name` (str) — name to greet; must be non-empty

**Output:**
- Returns str of form "Hello, {name}!"

**Exceptions:**
- `ValueError("Name cannot be empty")` if name is falsy

**Example:**
```python
hello("Alice")  # Returns: "Hello, Alice!"
hello("")       # Raises: ValueError("Name cannot be empty")
```

### 5.2 Backend API Interface

**Endpoint:** `POST /api/greet`

**Request:**

```json
{
  "name": "string (required)"
}
```

**Response (200 OK):**

```json
{
  "greeting": "string"
}
```

**Response (400 Bad Request):**

```json
{
  "detail": "string"
}
```

**Example:**

Request:
```bash
curl -X POST http://localhost:8000/api/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

Response (200):
```json
{"greeting": "Hello, Alice!"}
```

### 5.3 Frontend-to-Backend Interface

**Protocol:** HTTP/JSON  
**Implementation:** `frontend/src/api.ts` (typed fetch wrapper)  

**TypeScript Types:**

```typescript
interface GreetRequest { name: string }
interface GreetResponse { greeting: string }
async function greet(name: string): Promise<GreetResponse>
```

### 5.4 Backend-to-Core Module Interface

**Type:** Direct function call  
**Implementation:** `backend/app/greeting.py` re-exports `hello()` from `src.hello`  
**Mechanism:** Python import statement: `from src.hello import hello`

## 6. Data Structures

### 6.1 Greeting Data

**Type:** String  
**Format:** "Hello, {name}!"  
**Constraints:**
- Must contain supplied name
- Must start with "Hello"
- Must end with "!"
- Generated by SCI-001's `hello()` function

**Example:** "Hello, Alice!"

### 6.2 Request/Response Models

**GreetRequest (Pydantic)**

| Field | Type | Required | Constraints |
|---|---|---|---|
| `name` | str | Yes | Non-empty (validated by backend) |

**GreetResponse (Pydantic)**

| Field | Type | Required | Constraints |
|---|---|---|---|
| `greeting` | str | Yes | Valid greeting (generated by SCI-001) |

**ErrorResponse (implicit)**

| Field | Type | Required | Constraints |
|---|---|---|---|
| `detail` | str | Yes | Error message from backend |

## 7. Processing and Control Flow

### 7.1 Happy Path: Valid Greeting Request

```
1. User enters name in frontend form
2. User clicks "Get Greeting" button
3. Frontend calls greet(name) — sends POST /api/greet with JSON
4. Backend receives request, Pydantic validates
5. Backend calls hello(request.name)
6. SCI-001 validates name, generates greeting
7. SCI-001 returns greeting string
8. Backend wraps in GreetResponse, returns HTTP 200
9. Frontend receives response, displays greeting
10. Frontend clears input field
```

**Evidence:** `frontend/src/App.tsx:11-26` (submission handler) → `api.ts:11-26` (API call) → `backend/app/main.py:29-36` (endpoint) → `src/hello.py:15-30` (core logic)

### 7.2 Error Path: Empty Name

```
1. User enters empty name or leaves input blank
2. User clicks "Get Greeting" button
3. Frontend calls greet("") — sends POST /api/greet with {"name": ""}
4. Backend receives request, Pydantic validates
5. Backend calls hello("")
6. SCI-001 validates: name is falsy, raises ValueError
7. Backend catches ValueError, raises HTTPException(400, detail=str(error))
8. Backend returns HTTP 400 with {"detail": "Name cannot be empty"}
9. Frontend's api.ts catches non-2xx response, throws Error with detail
10. Frontend's App catches error, displays error message
```

**Evidence:** `frontend/src/App.tsx:22` (error catch) → `api.ts:20-22` (error parsing) → `backend/app/main.py:35-36` (error handling) → `src/hello.py:27-28` (validation)

### 7.3 Error Path: Network Failure

```
1. User submits form
2. Frontend attempts HTTP request
3. Network failure (offline, server down, etc.)
4. Fetch throws or response fails
5. Frontend catches in try-catch, displays generic error
```

**Evidence:** `frontend/src/App.tsx:21-22` (generic error handling)

## 8. Error Handling

### 8.1 Core Module (SCI-001)

**Strategy:** Fail-fast validation with exception

| Condition | Action | Result |
|---|---|---|
| Empty/None name | Raise `ValueError` | Caller must handle exception |
| Valid name | Generate greeting | Return string |

### 8.2 Backend API (SCI-002)

**Strategy:** Catch core exceptions, translate to HTTP errors

| Source | Caught Exception | Translation | HTTP Response |
|---|---|---|---|
| SCI-001 | `ValueError` | FastAPI HTTPException | 400 Bad Request + detail |
| Pydantic | `ValidationError` | FastAPI auto-handled | 400 Bad Request |
| Other | Unhandled | FastAPI 500 | 500 Internal Server Error |

**Evidence:** `backend/app/main.py:35-36`

### 8.3 Frontend (SCI-003)

**Strategy:** Display user-friendly error messages

| Error Source | Handling | User Display |
|---|---|---|
| HTTP error response | Parse error.detail | "Error: {detail}" |
| Network failure | Catch fetch error | "Error: {generic message}" |
| Type error | Fallback message | "Error: An error occurred" |

**Evidence:** `frontend/src/api.ts:20-22`, `frontend/src/App.tsx:52-55`

## 9. Safety Design

**Classification:** EVIDENCE + MISSING / HUMAN REVIEW REQUIRED  

**Current Status:**
- No formal safety analysis or safety requirements documented
- SCI-001 labeled "safety-critical" in `docs/design.md` but no supporting analysis
- No automated safety testing

**Design Elements for Robustness:**
- **Input validation at multiple layers** (defense in depth)
- **Type checking** (Python type hints, TypeScript, Pydantic)
- **Error propagation** (exceptions preserved with context)

**Missing for Safety Certification:**
- Hazard analysis
- Safety requirements traceability
- Safety-critical test cases
- Formal verification

## 10. Security Design

**Classification:** EVIDENCE + PROPOSED / HUMAN REVIEW REQUIRED  

### 10.1 Implemented Controls

**Input Validation:**
- SCI-001 validates non-empty name
- SCI-002 uses Pydantic to validate request shape and types

**CORS Configuration:**
- Hardcoded to development-only origins (localhost:5173, localhost:3000)
- Appropriate for development; **NOT suitable for production**

**Type Checking:**
- TypeScript enforces types at compile time (frontend)
- Python type hints and Pydantic enforce types at runtime (backend)

### 10.2 Security Gaps

| Gap | Severity | Impact |
|---|---|---|
| CORS hardcoded to localhost | HIGH | Production deployment unsafe |
| No authentication/authorization | MEDIUM | All requests accepted |
| No rate limiting | MEDIUM | Susceptible to DoS |
| No HTTPS enforcement | MEDIUM | Unencrypted communication in transit |
| No input sanitization beyond validation | LOW | XSS risk if greeting stored and redisplayed |

### 10.3 Security Recommendations

**Before Production:**
1. Configure CORS to production domain(s) only
2. Add HTTPS enforcement (TLS/SSL)
3. Implement rate limiting or API gateway controls
4. Add authentication if required by use case
5. Security review of error messages (no information leakage)

## 11. Performance Design

**Classification:** PROPOSED / HUMAN REVIEW REQUIRED  

**Current Characteristics:**
- No performance requirements specified
- Core module is CPU-bound: string validation and formatting only
- No I/O, database, or network calls within SCI-001
- Request latency dominated by HTTP round-trip and middleware processing

**Performance Considerations:**
- Single-threaded FastAPI (default Uvicorn workers)
- No connection pooling or caching
- No asynchronous I/O in core module
- Stateless design (each request independent)

**Optimization Opportunities (not yet implemented):**
- Multi-worker Uvicorn deployment
- Response caching (if semantically appropriate)
- Compression (gzip for large response bodies)
- CDN for static frontend assets
- Load balancing (if horizontal scaling required)

## 12. External Dependencies

| Dependency | Type | Version | Purpose |
|---|---|---|---|
| FastAPI | Framework | 0.24.x | HTTP REST API |
| Pydantic | Validation | 2.x | Request/response schema |
| Uvicorn | ASGI Server | 0.24.x | HTTP server |
| React | Framework | 18 | Frontend UI |
| TypeScript | Language | 5.x | Frontend type checking |
| Vite | Build Tool | Latest | Frontend build & dev server |
| Pytest | Testing | 7.x | Test execution |
| Pytest-Cov | Tool | 7.x | Code coverage reporting |

## 13. Design Decisions

### Decision 1: Layered Architecture

**Status:** VERIFIED / EVIDENCE  
**Rationale:** Separates concerns (core logic, API, UI). Enables independent testing and deployment.  
**Alternative:** Monolithic or microservices — rejected as over-engineered for demonstration.  
**Evidence:** `docs/design.md`, observed source code structure

### Decision 2: FastAPI + Pydantic for Backend

**Status:** EVIDENCE  
**Rationale:** Modern Python framework with built-in validation and type support.  
**Alternative:** Flask, Django, etc. — FastAPI chosen for type safety and developer experience.  
**Evidence:** `backend/app/main.py`

### Decision 3: React for Frontend

**Status:** EVIDENCE  
**Rationale:** Industry-standard component-based SPA framework with TypeScript support.  
**Alternative:** Vue, Angular, Svelte, etc. — React chosen for ecosystem and community.  
**Evidence:** `frontend/src/App.tsx`

### Decision 4: Direct Function Call Between Backend and Core

**Status:** EVIDENCE  
**Rationale:** Simplicity for demonstration; avoids IPC overhead.  
**Alternative:** Separate service, gRPC, message queue — rejected as unnecessary.  
**Evidence:** `backend/app/greeting.py`

### Decision 5: No Frontend Automated Tests

**Status:** EVIDENCE + FINDING  
**Rationale:** Out of scope for v1.0.0 (manual testing sufficient for demonstration).  
**Alternative:** Add Vitest, Playwright, or Cypress — recommended for future.  
**Evidence:** `docs/design.md` section 7, no test files in `frontend/src/`

## 14. Requirements Allocation

**All functional requirements allocated to software components:**

| SWR | Requirement | SCI | Component | Implementation |
|---|---|---|---|---|
| SWR-001 | Greeting contains name | SCI-001 | `hello()` function | `src/hello.py:30` |
| SWR-002 | "Hello" prefix | SCI-001 | `DEFAULT_GREETING` | `src/hello.py:12` |
| SWR-003 | Input validation | SCI-001 | Validation check | `src/hello.py:27-28` |
| SWR-004 | Exclamation mark | SCI-001 | Format string | `src/hello.py:30` |
| SWR-005 | POST /api/greet | SCI-002 | Endpoint handler | `backend/app/main.py:29-36` |
| SWR-006 | API greeting format | SCI-002 | GreetResponse model | `backend/app/main.py:14-15` |
| SWR-007 | API input validation | SCI-002 | Error handler | `backend/app/main.py:35-36` |
| SWR-008 | /health endpoint | SCI-002 | Health check function | `backend/app/main.py:39-42` |
| SWR-009 | Form UI | SCI-003 | Form JSX | `frontend/src/App.tsx:32-44` |
| SWR-010 | POST to backend | SCI-003 | API client | `frontend/src/api.ts:11-26` |
| SWR-011 | Display greeting | SCI-003 | Success result | `frontend/src/App.tsx:46-49` |
| SWR-012 | Display error | SCI-003 | Error result | `frontend/src/App.tsx:52-55` |
| SWR-013 | Loading state | SCI-003 | UI feedback | `frontend/src/App.tsx:39, 41-42` |
| SWR-014 | Clear input | SCI-003 | Form reset | `frontend/src/App.tsx:20` |

## 15. Open Issues

1. **Frontend Testing** — No automated tests. Manual only. (Recommended: add Vitest + Playwright)
2. **REQ-005 Implementation** — Logging not implemented. Planned for future?
3. **Production Deployment** — CORS, HTTPS, and authentication model undefined
4. **Safety Justification** — SCI-001 labeled safety-critical without supporting analysis
5. **Performance Baseline** — No performance requirements or baseline metrics defined

## 16. Traceability

**Requirement-to-Implementation Traceability:**

All SWRs traced to source code locations and test evidence. See Section 14 (Requirements Allocation) for complete mapping.

**Design-to-Implementation Traceability:**

All design elements are observable in source code:
- SCI-001 behavior directly observable in `src/hello.py`
- SCI-002 design reflected in `backend/app/` structure and code
- SCI-003 design evident in `frontend/src/App.tsx` and `api.ts`

## 17. Review Status

**Status:** DRAFT — Human engineering review required

**Review Checklist:**
- [ ] Software architecture approved
- [ ] Component responsibilities confirmed
- [ ] Design decisions endorsed
- [ ] Security assumptions acceptable
- [ ] Performance characteristics adequate
- [ ] Safety design (if applicable) reviewed
- [ ] Implementation code matches design
- [ ] Test coverage adequate

---

**Document Generated By:** System Design QMS Assistant  
**Generation Date:** 2026-09-02  
**Evidence Authority:** EVIDENCE (observed implementation in `src/`, `backend/`, `frontend/`)  
**Classification:** DRAFT — Human review and approval required before design baseline
