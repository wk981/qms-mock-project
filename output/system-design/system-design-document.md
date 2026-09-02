# System Design Document

**Status:** DRAFT  
**Project:** Hello Project  
**Generated:** 2026-09-02  
**Revision:** 1.0  

## 1. Purpose

This document describes the system design for the Hello Project, a demonstration application combining a DTE (Development, Test & Evaluation) evidence module with a fullstack web application architecture. The design allocates system requirements to software configuration items and describes the architectural approach.

## 2. Scope

This design covers:
- The greeting operation core logic (SCI-001)
- The REST API interface exposing the greeting over HTTP (SCI-002)
- The web-based user interface (SCI-003)
- Integration between layers and external dependencies

This design does **not** cover:
- Deployment infrastructure or containerization
- Security hardening beyond CORS configuration
- Performance optimization or scaling strategies

## 3. Requirements Baseline

**Source:** `docs/requirements.md`  
**Authority:** VERIFIED  
**Status:** Approved  

| Requirement | Title | Type | Allocated To | Status |
|---|---|---|---|---|
| REQ-001 | Greeting | Functional | SCI-001 | Implemented |
| REQ-002 | Default Greeting | Functional | SCI-001 | Implemented |
| REQ-003 | Input Validation | Functional | SCI-001 | Implemented |
| REQ-004 | Punctuation | Functional | SCI-001 | Implemented |
| REQ-005 | Logging | Functional | — | Not implemented |
| REQ-006 | Greeting API | Functional | SCI-002 | Implemented |
| REQ-007 | API Input Validation | Functional | SCI-002 | Implemented |
| REQ-008 | Greeting Web Interface | Functional | SCI-003 | Implemented |

**Note:** REQ-005 is a known gap. The requirement exists in the baseline but is explicitly not implemented in v1.0.0.

## 4. System Overview

The Hello Project is a three-layer fullstack web application:

1. **Frontend Layer** — React/TypeScript browser-based UI
2. **API Layer** — FastAPI HTTP REST service
3. **Core Logic Layer** — Pure Python module with greeting generation logic

**Design Principle:** Separation of concerns. Each layer is independently testable and has a well-defined responsibility.

## 5. System Architecture

### 5.1 Architectural Pattern

**Type:** Layered (3-tier) architecture  
**Evidence:** `docs/design.md` section 1, `README.md` Architecture section  

```
┌──────────────────────────────────────────────┐
│  Frontend (React/TypeScript, Browser)        │
│  src/App.tsx, src/api.ts                     │
└─────────────────┬──────────────────────────┘
                  │
        HTTP POST /api/greet
        { "name": "string" }
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  Backend (FastAPI, Python 3.11)              │
│  backend/app/main.py                         │
│  • Request validation                        │
│  • Response formatting                       │
│  • Error handling                            │
└─────────────────┬──────────────────────────┘
                  │
        Function call: hello(name)
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  Core Module (Pure Python)                   │
│  src/hello.py                                │
│  • Greeting generation                       │
│  • Input validation                          │
└──────────────────────────────────────────────┘
```

**Classification:** EVIDENCE — `docs/design.md` section 1 and observed implementation  

### 5.2 System Boundaries

**External Systems:** None. This is a self-contained demonstration application.  

**External Dependencies:**
- **Frontend:** React 18, Vite, TypeScript (EVIDENCE: `frontend/package.json`)
- **Backend:** FastAPI, Pydantic, Uvicorn (EVIDENCE: `backend/requirements.txt`)
- **Core:** Python 3.11+ standard library only (EVIDENCE: `src/hello.py`)

## 6. System Components

### 6.1 Component Inventory

| Component | Layer | Technology | Responsibility |
|---|---|---|---|
| Core Module (SCI-001) | Core Logic | Python | Greeting generation, input validation |
| Backend API (SCI-002) | API | FastAPI/Pydantic | HTTP routing, validation, response formatting |
| Frontend App (SCI-003) | Frontend | React/TypeScript | User input, API communication, result display |

## 7. Software Configuration Items

### 7.1 SCI-001 — Core Greeting Module

**Location:** `src/hello.py`  
**Language:** Python 3  
**Classification:** EVIDENCE — observed implementation  

**Responsibilities:**
- Generate greeting text containing supplied name
- Use "Hello" as default greeting prefix
- Validate non-empty name input
- Format greeting with exclamation mark punctuation

**Interface:**
```python
def hello(name: str) -> str
    """Return a greeting for name.
    
    Args:
        name: The name to greet (non-empty string)
    
    Returns:
        A greeting of the form "Hello, <name>!"
    
    Raises:
        ValueError: If name is empty
    """
```

**Requirements Allocated:** REQ-001, REQ-002, REQ-003, REQ-004  

**Tests:** `tests/test_hello.py` (4 tests), `backend/tests/test_greeting.py` (4 tests)  
**Evidence:** Observed source code and test execution in CI pipeline  

### 7.2 SCI-002 — FastAPI Application

**Location:** `backend/app/main.py`  
**Language:** Python 3.11  
**Framework:** FastAPI with Pydantic validation  
**Classification:** EVIDENCE — observed implementation  

**Responsibilities:**
- Accept HTTP POST requests to `/api/greet`
- Parse and validate JSON request body (Pydantic models)
- Call core module's `hello()` function
- Return greeting or error response in JSON format
- Translate `ValueError` exceptions to HTTP 400 responses
- Provide `/health` endpoint for liveness checks

**Interfaces:**

**POST /api/greet**
- Request: `{"name": "string"}`
- Response (200): `{"greeting": "Hello, <name>!"}`
- Response (400): `{"detail": "Name cannot be empty"}`

**GET /health**
- Response (200): `{"status": "ok"}`

**Requirements Allocated:** REQ-006, REQ-007  

**Tests:** `backend/tests/test_main.py` (3 API integration tests)  
**CORS Configuration:** Allows requests from `localhost:5173` (frontend dev) and `localhost:3000`  
**Evidence:** Source code at `backend/app/main.py`, CI pipeline test execution  

### 7.3 SCI-003 — React Frontend Application

**Location:** `frontend/src/App.tsx`  
**Language:** TypeScript / React 18  
**Build Tool:** Vite  
**Classification:** EVIDENCE — observed implementation  

**Responsibilities:**
- Render form UI with name input field
- Handle form submission events
- Send HTTP POST request to backend API
- Display greeting result to user
- Display error messages and validation feedback
- Manage loading state during API request

**User Interface Elements:**
- Text input field (placeholder: "Enter your name")
- Submit button ("Get Greeting")
- Result display area (green for success, red for error)
- Loading state feedback

**Requirements Allocated:** REQ-008  

**Testing:** Manual exploratory testing only (no automated tests)  
**Evidence:** Source code at `frontend/src/App.tsx`, successful TypeScript compilation in CI pipeline  

## 8. Functional Allocation

| Requirement | Allocated To | Design Element | Implementation | Verification |
|---|---|---|---|---|
| REQ-001 | SCI-001 | `hello()` function | `src/hello.py:15-30` | `tests/test_hello.py:11-13` |
| REQ-002 | SCI-001 | `DEFAULT_GREETING` constant | `src/hello.py:12` | `tests/test_hello.py:16-18` |
| REQ-003 | SCI-001 | Input validation check | `src/hello.py:27-28` | `tests/test_hello.py:21-24` |
| REQ-004 | SCI-001 | Punctuation in format string | `src/hello.py:30` | `tests/test_hello.py:27-29` |
| REQ-005 | — | Logging system | Not implemented | Not implemented |
| REQ-006 | SCI-002 | POST /api/greet endpoint | `backend/app/main.py:29-36` | `backend/tests/test_main.py:12-20` |
| REQ-007 | SCI-002 | Pydantic validation, error handling | `backend/app/main.py:10-11, 35-36` | `backend/tests/test_main.py:23-28` |
| REQ-008 | SCI-003 | Form UI, API client, result display | `frontend/src/App.tsx` | Manual testing |

## 9. Interfaces

### 9.1 Core Module Interface (SCI-001)

**Function:** `hello(name: str) -> str`  
**Evidence:** `src/hello.py`  
**Classification:** VERIFIED — specified in `docs/design.md` section 3  

### 9.2 REST API Interface (SCI-002 to External Clients)

**Endpoint:** `POST /api/greet`  
**Evidence:** `backend/app/main.py:29-36`  
**Classification:** VERIFIED — specified in `docs/requirements.md` REQ-006 and `docs/design.md` section 4  

**Request Schema:**
```json
{
  "name": "string"
}
```

**Response Schema (200 OK):**
```json
{
  "greeting": "string"
}
```

**Response Schema (400 Bad Request):**
```json
{
  "detail": "string"
}
```

### 9.3 Backend-to-Frontend Interface (SCI-002 to SCI-003)

**Protocol:** HTTP with JSON  
**Implementation:** `frontend/src/api.ts`  
**Classification:** EVIDENCE — observed implementation  

**Client Library:** Typed TypeScript fetch wrapper with error handling  

### 9.4 Backend-to-Core Interface (SCI-002 to SCI-001)

**Method:** Direct function call via `backend/app/greeting.py`  
**Implementation:** `backend/app/greeting.py` re-exports `hello()` from `src.hello`  
**Classification:** EVIDENCE — observed implementation  

## 10. Data Flow

```
User Input (browser)
    │
    ▼
App.tsx (capture name)
    │
    ├─► Set loading state
    │
    ▼
api.ts (fetch POST /api/greet)
    │
    ├─► HTTP POST with { "name": "Alice" }
    │
    ▼
FastAPI (backend/app/main.py)
    │
    ├─► Parse GreetRequest (Pydantic validation)
    │
    ├─► Try: hello(request.name)
    │
    ▼
hello() function (src/hello.py)
    │
    ├─► Validate name not empty
    │
    ├─► Format greeting string
    │
    ▼
Return greeting to FastAPI
    │
    ├─► Wrap in GreetResponse
    │
    ├─► HTTP 200 + JSON
    │
    ▼
fetch() in api.ts
    │
    ├─► Parse response
    │
    ▼
App.tsx (display result)
    │
    └─► Render in success/error area
```

## 11. Performance Considerations

**Classification:** PROPOSED / HUMAN REVIEW REQUIRED  

The current design has no explicit performance requirements. Observations:

- The greeting operation is CPU-bound by input validation and string formatting only — no I/O or database access
- Response time should be dominated by HTTP latency between browser and backend
- No caching, rate limiting, or async batching is currently implemented
- CORS is configured for development-only localhost origins; production deployment would need review

**Design Decision:** Performance optimization is deferred pending deployment and operational profiling.

## 12. Security Considerations

**Classification:** EVIDENCE + PROPOSED / HUMAN REVIEW REQUIRED  

**Implemented Controls:**
- Input validation at both core and API layers (REQ-003, REQ-007)
- CORS middleware configured for localhost development (EVIDENCE: `backend/app/main.py:20-26`)
- Pydantic validation enforces type and shape of incoming JSON (EVIDENCE: `backend/app/main.py:10-11`)

**Design Gaps:**
- CORS is currently hardcoded to `localhost:5173` and `localhost:3000` — **NOT suitable for production**
- No authentication or authorization implemented
- No rate limiting or DDoS protection
- Frontend stores no credentials, but no HTTPS enforcement is documented

**Proposed Actions:**
- Before production deployment, security review of CORS policy, authentication requirements, and protocol enforcement (HTTPS)
- Implement rate limiting or API gateway controls if exposed to untrusted clients

## 13. Safety Considerations

**Classification:** EVIDENCE + MISSING / HUMAN REVIEW REQUIRED  

**Current Classification:**  
The design document (`docs/design.md`) labels SCI-001 as "Safety-critical." However:

1. No formal safety analysis (hazard analysis, hazard log, safety requirements traceability) is present in the project
2. No indication of regulatory or certification requirements
3. The application is documented as a demonstration/example project

**Finding:** SCI-001 is labeled safety-critical in the design but lacks supporting safety analysis. Clarification required: Is safety classification appropriate, and if so, what safety analysis is required?

**Verification:** No automated safety testing or formal verification is evident.

## 14. Design Constraints

| Constraint | Source | Impact |
|---|---|---|
| Python 3.11+ | `README.md` Prerequisites | Backend must run on Python 3.11 or later |
| Node.js 18+ | `README.md` Prerequisites | Frontend build and dev server require Node.js 18+ |
| Localhost development | `CORS allow_origins` | Dev environment limited to localhost; production requires configuration change |
| Single-purpose function | Design philosophy | Core module handles greeting only; other operations require separate modules |

## 15. Assumptions

| Assumption | Evidence | Validity |
|---|---|---|
| Core module receives non-null input | Validated by `src/hello.py` type hint `name: str` and guard clause | Type checking enforced; assumption holds |
| Backend can import core module | Python path configured to include parent of `src/` | EVIDENCE: `backend/app/greeting.py` successfully imports `from src.hello import hello` |
| Frontend runs on localhost:5173 by default | Vite dev server standard port | Standard Vite behavior |
| CORS not needed for production | Current configuration hardcoded for localhost | **ASSUMPTION: Production will configure CORS appropriately** |

## 16. Architecture and Design Decisions

### Decision 1: Layered (3-tier) Architecture

**Status:** VERIFIED / EVIDENCE  
**Rationale:** Separates concerns (core logic, API exposure, user interface). Allows independent testing and deployment of layers.  
**Evidence:** Documented in `docs/design.md` section 1; implemented across `src/`, `backend/`, and `frontend/` directories  

### Decision 2: Direct Function Call Between Backend and Core

**Status:** EVIDENCE  
**Rationale:** Avoids inter-process communication overhead for a demonstration project. Simplifies testing and debugging.  
**Evidence:** `backend/app/greeting.py` imports and calls `hello()` directly  

### Decision 3: Pydantic for API Request Validation

**Status:** EVIDENCE  
**Rationale:** Provides automatic validation, type checking, and error response generation.  
**Evidence:** `backend/app/main.py:10-11` (GreetRequest, GreetResponse models)  

### Decision 4: Manual Testing for Frontend (SCI-003)

**Status:** EVIDENCE + PROPOSED / HUMAN REVIEW REQUIRED  
**Rationale:** No frontend test framework currently configured.  
**Evidence:** `docs/design.md` section 7 states "SCI-003 has no automated test suite"  
**Proposed Action:** Consider adding Vitest or Playwright for automated frontend testing in a future iteration.

## 17. Requirements Allocation

**All functional requirements are allocated:**
- REQ-001 through REQ-004 → SCI-001 (core module)
- REQ-005 → unallocated (intentional gap)
- REQ-006, REQ-007 → SCI-002 (backend API)
- REQ-008 → SCI-003 (frontend UI)

**Allocation Status:** 7 of 8 requirements allocated. REQ-005 (Logging) is explicitly not implemented in v1.0.0.

## 18. Open Issues

1. **REQ-005 Logging Implementation** — Not implemented. Planned for future release?
2. **Frontend Automated Testing** — SCI-003 lacks test suite. Manual testing only.
3. **Safety Classification Clarification** — SCI-001 marked safety-critical in design; no supporting safety analysis.
4. **Production CORS Configuration** — Current hardcoded for localhost; production deployment undefined.
5. **Authentication and Authorization** — No security model defined; assumed out-of-scope for demonstration.

## 19. Design Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| REQ-005 unimplemented | High | Incomplete feature set; logging unavailable for debugging | Planned for future release; documented as known gap |
| Frontend lacks tests | High | Regression risk when UI changes; incomplete verification of REQ-008 | Manual testing followed by automated test framework addition |
| Safety classification unsupported | Medium | If real safety-critical use found, design is inadequate | Formal safety analysis required before safety-critical deployment |
| CORS hardcoded to localhost | High | Current design unsuitable for production; requires manual reconfiguration | Document production CORS policy as prerequisite |

## 20. Traceability

**Evidence-Based Traceability:**

All design elements are traceable to verified requirements and observed implementation. See Section 8 (Functional Allocation) for requirement-to-SCI-to-implementation mapping.

**RTM Generation:** See separate `requirements-traceability-matrix.md`

## 21. Review Status

**Draft Status:** ✓ DRAFT  
**Authority:** Assistant-generated; not yet reviewed  
**Next Step:** Engineering review and approval required before design baseline is established  

**Review Checklist:**
- [ ] Requirements baseline confirmed accurate
- [ ] Architectural approach approved
- [ ] Design allocations reviewed
- [ ] Safety classification confirmed (or corrected)
- [ ] Performance and security assumptions acceptable
- [ ] Design risks acceptable or mitigated
- [ ] Design ready for implementation/DTE phase

---

**Document Generated By:** System Design QMS Assistant  
**Generation Date:** 2026-09-02  
**Baseline Authority:** VERIFIED `docs/requirements.md`  
**Implementation Evidence:** EVIDENCE (observed source code, tests, CI)  
**Classification:** DRAFT — Human review and approval required
