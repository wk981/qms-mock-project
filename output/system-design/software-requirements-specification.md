# Software Requirements Specification

**Status:** DRAFT  
**Project:** Hello Project  
**Generated:** 2026-09-02  
**Baseline:** System Requirements (REQ-001 through REQ-008)  

## 1. Introduction

This document specifies the software requirements for the Hello Project derived from the verified system requirements in `docs/requirements.md`. Each software requirement (SWR-*) is traced to its parent system requirement and specifies what the software must do to satisfy that requirement.

**Derivation Approach:** System requirements are analyzed and allocated to software configuration items (SCI-001, SCI-002, SCI-003). Each SCI has corresponding software requirements.

## 2. SCI-001: Core Greeting Module Requirements

### SWR-001

**Parent Requirement:** REQ-001 (Greeting)  
**Description:** The `hello()` function shall return a greeting containing the supplied name.  
**Rationale:** Core functionality must incorporate the user's name into the greeting output.  
**Source:** REQ-001; EVIDENCE: `src/hello.py:15-30`, test `tests/test_hello.py:11-13`  
**Verification:** Unit test `test_greeting_contains_name()` asserts supplied name is present in output  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-002

**Parent Requirement:** REQ-002 (Default Greeting)  
**Description:** The `hello()` function shall use "Hello" as the default greeting prefix.  
**Rationale:** Standardized greeting format as specified in requirements.  
**Source:** REQ-002; EVIDENCE: `src/hello.py:12` (DEFAULT_GREETING constant), test `tests/test_hello.py:16-18`  
**Verification:** Unit test `test_default_greeting()` asserts greeting begins with "Hello"  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-003

**Parent Requirement:** REQ-003 (Input Validation)  
**Description:** The `hello()` function shall raise `ValueError` if the supplied name is empty or falsy.  
**Rationale:** Empty input validation prevents malformed greetings.  
**Source:** REQ-003; EVIDENCE: `src/hello.py:27-28`, test `tests/test_hello.py:21-24`  
**Verification:** Unit test `test_empty_name_is_rejected()` asserts `ValueError` is raised  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-004

**Parent Requirement:** REQ-004 (Punctuation)  
**Description:** The `hello()` function shall end the greeting with an exclamation mark (`!`).  
**Rationale:** Standardized greeting format.  
**Source:** REQ-004; EVIDENCE: `src/hello.py:30`, test `tests/test_hello.py:27-29`  
**Verification:** Unit test `test_greeting_ends_with_exclamation_mark()` asserts final character is `!`  
**Safety Relevance:** None  
**Status:** Implemented  

## 3. SCI-001: Requirements Status

| SWR | Requirement | Implemented | Tested | Status |
|---|---|---|---|---|
| SWR-001 | Greeting contains name | ✓ | ✓ | Implemented |
| SWR-002 | Default "Hello" prefix | ✓ | ✓ | Implemented |
| SWR-003 | Input validation | ✓ | ✓ | Implemented |
| SWR-004 | Exclamation mark punctuation | ✓ | ✓ | Implemented |

## 4. SCI-002: Backend API Requirements

### SWR-005

**Parent Requirement:** REQ-006 (Greeting API)  
**Description:** The backend shall expose a POST endpoint at `/api/greet` that accepts a JSON request body containing a `name` field and returns a JSON response containing a `greeting` field.  
**Rationale:** REQ-006 requires HTTP REST API exposure of the greeting operation.  
**Source:** REQ-006; EVIDENCE: `backend/app/main.py:29-36`, test `backend/tests/test_main.py:12-20`  
**Verification:** API integration test `test_greet_success()` asserts HTTP 200, JSON response with greeting field  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-006

**Parent Requirement:** REQ-006 (Greeting API)  
**Description:** The greeting returned by the `/api/greet` endpoint shall satisfy SWR-001, SWR-002, SWR-003, and SWR-004 (i.e., contain the name, begin with "Hello", reject empty input, end with exclamation mark).  
**Rationale:** API response must satisfy the same constraints as the core function.  
**Source:** REQ-006 + REQ-001 through REQ-004; EVIDENCE: `backend/app/greeting.py` wrapper, test `backend/tests/test_main.py:12-20` asserts response contains name, starts with "Hello", ends with "!"  
**Verification:** API test validates greeting format matches core module constraints  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-007

**Parent Requirement:** REQ-007 (API Input Validation)  
**Description:** The backend shall validate the `name` field in the request body and return an HTTP 400 response with an error detail message if the name is empty or missing.  
**Rationale:** Input validation at API boundary prevents invalid requests from reaching the core module.  
**Source:** REQ-007; EVIDENCE: `backend/app/main.py:10-11` (Pydantic GreetRequest), `backend/app/main.py:35-36` (error handling), test `backend/tests/test_main.py:23-28`  
**Verification:** API test `test_greet_empty_name()` asserts HTTP 400 with error detail  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-008

**Parent Requirement:** REQ-006 (Greeting API)  
**Description:** The backend shall provide a `/health` endpoint that returns HTTP 200 with `{"status": "ok"}` to indicate the service is alive.  
**Rationale:** Health check endpoint enables monitoring and load balancer integration.  
**Source:** REQ-006 (API), EVIDENCE: `backend/app/main.py:39-42`, test `backend/tests/test_main.py:31-35`  
**Verification:** API test `test_health_check()` asserts HTTP 200 and correct response body  
**Safety Relevance:** None  
**Status:** Implemented  

## 5. SCI-002: Requirements Status

| SWR | Requirement | Implemented | Tested | Status |
|---|---|---|---|---|
| SWR-005 | POST /api/greet endpoint | ✓ | ✓ | Implemented |
| SWR-006 | API greeting satisfies core constraints | ✓ | ✓ | Implemented |
| SWR-007 | API input validation + 400 response | ✓ | ✓ | Implemented |
| SWR-008 | GET /health endpoint | ✓ | ✓ | Implemented |

## 6. SCI-003: Frontend UI Requirements

### SWR-009

**Parent Requirement:** REQ-008 (Greeting Web Interface)  
**Description:** The frontend shall provide an HTML form with a text input field for the user's name and a submit button.  
**Rationale:** REQ-008 requires a user interface for submitting a name.  
**Source:** REQ-008; EVIDENCE: `frontend/src/App.tsx:32-44` (form with input and button)  
**Verification:** Manual exploratory testing of the web UI  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-010

**Parent Requirement:** REQ-008 (Greeting Web Interface)  
**Description:** The frontend shall send an HTTP POST request to `/api/greet` with the user's name when the form is submitted.  
**Rationale:** Connects UI to backend API.  
**Source:** REQ-008; EVIDENCE: `frontend/src/api.ts:11-26` (fetch POST), `frontend/src/App.tsx:17-20` (submit handler calls greet)  
**Verification:** Manual testing: enter name, submit form, observe HTTP POST in browser network tab  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-011

**Parent Requirement:** REQ-008 (Greeting Web Interface)  
**Description:** The frontend shall display the greeting returned by the backend API in a result area on the page.  
**Rationale:** User must see the result of the greeting operation.  
**Source:** REQ-008; EVIDENCE: `frontend/src/App.tsx:46-49` (success result display)  
**Verification:** Manual testing: submit valid name, observe greeting displayed in success result area  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-012

**Parent Requirement:** REQ-008 (Greeting Web Interface)  
**Description:** The frontend shall display error messages returned by the backend API if the request fails.  
**Rationale:** User must be informed of input validation errors or other failures.  
**Source:** REQ-008; EVIDENCE: `frontend/src/api.ts:20-22` (error extraction), `frontend/src/App.tsx:52-55` (error result display)  
**Verification:** Manual testing: submit empty name, observe error message displayed in error result area  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-013

**Parent Requirement:** REQ-008 (Greeting Web Interface)  
**Description:** The frontend shall provide visual feedback indicating when an API request is in progress (e.g., loading state).  
**Rationale:** User experience: inform user that the application is waiting for the server response.  
**Source:** REQ-008; EVIDENCE: `frontend/src/App.tsx:9, 15, 24` (loading state), `frontend/src/App.tsx:39, 41-42` (disabled input/button with "Loading..." text during request)  
**Verification:** Manual testing: submit form, observe button text changes to "Loading..." while request is in flight  
**Safety Relevance:** None  
**Status:** Implemented  

### SWR-014

**Parent Requirement:** REQ-008 (Greeting Web Interface)  
**Description:** The frontend shall clear the input field after a successful greeting submission.  
**Rationale:** User experience: prepare form for the next greeting.  
**Source:** REQ-008; EVIDENCE: `frontend/src/App.tsx:20` (setName('') after success)  
**Verification:** Manual testing: submit valid name, observe input field cleared after greeting displayed  
**Safety Relevance:** None  
**Status:** Implemented  

## 7. SCI-003: Requirements Status

| SWR | Requirement | Implemented | Tested | Status |
|---|---|---|---|---|
| SWR-009 | Form with input field and button | ✓ | Manual | Implemented |
| SWR-010 | POST to /api/greet on submit | ✓ | Manual | Implemented |
| SWR-011 | Display greeting result | ✓ | Manual | Implemented |
| SWR-012 | Display error messages | ✓ | Manual | Implemented |
| SWR-013 | Loading state feedback | ✓ | Manual | Implemented |
| SWR-014 | Clear input after success | ✓ | Manual | Implemented |

## 8. Unallocated Requirements

### SWR-015 (Derived from REQ-005 — Logging)

**Parent Requirement:** REQ-005 (Logging)  
**Description:** The system shall record each greeting request in the application log with a log entry identifying the request.  
**Source:** REQ-005; EVIDENCE: `docs/requirements.md` section 2  
**Current Status:** **Not implemented in v1.0.0**  
**Evidence:** No logging framework integration found in `src/hello.py` or `backend/app/main.py`  
**Verification:** No automated tests for logging functionality  
**Safety Relevance:** None  
**Status:** Design gap — unimplemented (intentional)  

## 9. Software Requirement Summary

**Total Software Requirements Derived:** 15  
**Implemented:** 14  
**Not Implemented (Intentional Gap):** 1 (SWR-015 / REQ-005)  

| Category | Count |
|---|---|
| Core Module (SCI-001) | 4 implemented |
| Backend API (SCI-002) | 4 implemented |
| Frontend UI (SCI-003) | 6 implemented, manual testing |
| Unallocated / Gaps | 1 (logging) |

## 10. Verification Methods

| Verification Method | SWRs | Count |
|---|---|---|
| Automated unit test | SWR-001, SWR-002, SWR-003, SWR-004 | 4 |
| Automated API integration test | SWR-005, SWR-006, SWR-007, SWR-008 | 4 |
| Manual exploratory testing | SWR-009 through SWR-014 | 6 |
| Not implemented | SWR-015 | 1 |

**Classification:**
- **DERIVED** — SWRs are logically derived from VERIFIED system requirements
- **EVIDENCE** — Implementation and test code exists and was observed
- **NOT VERIFIED** — SWR-015 (logging) is unimplemented and unverified

## 11. Review Status

**Status:** DRAFT — Human review required  

This specification is generated from:
- VERIFIED: System requirements baseline (`docs/requirements.md`)
- EVIDENCE: Observed implementation (source code, tests, CI pipeline)
- DERIVED: Software requirements (logically derived by the QMS assistant)

All requirements are traceable to the verified system baseline and observed implementation evidence. No conflicting or ambiguous allocations.

---

**Document Generated By:** System Design QMS Assistant  
**Generation Date:** 2026-09-02  
**Derivation Authority:** VERIFIED system requirements `docs/requirements.md`  
**Implementation Authority:** EVIDENCE (observed source code and tests)  
**Classification:** DRAFT — Human review and approval required
