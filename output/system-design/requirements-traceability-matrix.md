# Requirements Traceability Matrix

**Status:** DRAFT  
**Project:** Hello Project  
**Generated:** 2026-09-02  
**Baseline:** System Requirements (REQ-001 through REQ-008)  

## 1. Purpose

This matrix traces the flow from system requirements through software requirements, design elements, implementation, and verification tests. It is the central artefact for demonstrating that:

- All requirements are implemented
- All implementations are tested
- All tests are traceable to requirements

## 2. RTM: System Requirements Level

| System Requirement | Description | Type | Allocated To | Software Requirements | Design Element | Implementation | Test Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| REQ-001 | Greeting contains supplied name | Functional | SCI-001 | SWR-001 | `hello()` function | `src/hello.py:15-30` | `tests/test_hello.py:11-13` | Fully Traced |
| REQ-002 | Default greeting is "Hello" | Functional | SCI-001 | SWR-002 | `DEFAULT_GREETING` constant | `src/hello.py:12` | `tests/test_hello.py:16-18` | Fully Traced |
| REQ-003 | Input validation rejects empty name | Functional | SCI-001 | SWR-003 | Validation check | `src/hello.py:27-28` | `tests/test_hello.py:21-24` | Fully Traced |
| REQ-004 | Greeting ends with exclamation mark | Functional | SCI-001 | SWR-004 | Format string | `src/hello.py:30` | `tests/test_hello.py:27-29` | Fully Traced |
| REQ-005 | Logging of greeting requests | Functional | — | SWR-015 | Not implemented | Not implemented | Not implemented | Design Gap |
| REQ-006 | Greeting API over HTTP REST | Functional | SCI-002 | SWR-005, SWR-006 | POST /api/greet endpoint | `backend/app/main.py:29-36` | `backend/tests/test_main.py:12-20` | Fully Traced |
| REQ-007 | API input validation and 400 error | Functional | SCI-002 | SWR-007 | Pydantic validation + error handling | `backend/app/main.py:10-11, 35-36` | `backend/tests/test_main.py:23-28` | Fully Traced |
| REQ-008 | Web-based user interface | Functional | SCI-003 | SWR-009 through SWR-014 | React form component | `frontend/src/App.tsx` | Manual exploratory testing | Fully Traced |

## 3. RTM: Software Requirements → Implementation → Tests

### SCI-001: Core Greeting Module

| Software Requirement | Description | Design Element | Implementation | Test | Verification Method | Status |
|---|---|---|---|---|---|---|
| SWR-001 | Greeting contains name | `hello()` return value | `src/hello.py:30`: f-string interpolation | `test_greeting_contains_name` | Assert name in result | Fully Traced |
| SWR-002 | Default "Hello" prefix | `DEFAULT_GREETING` constant | `src/hello.py:12`: `DEFAULT_GREETING = "Hello"` | `test_default_greeting` | Assert startswith("Hello") | Fully Traced |
| SWR-003 | Empty name rejection | Validation guard clause | `src/hello.py:27-28`: `if not name: raise ValueError` | `test_empty_name_is_rejected` | Assert ValueError raised | Fully Traced |
| SWR-004 | Exclamation mark suffix | Format string | `src/hello.py:30`: `f"{...}!"` | `test_greeting_ends_with_exclamation_mark` | Assert endswith("!") | Fully Traced |

### SCI-002: Backend API

| Software Requirement | Description | Design Element | Implementation | Test | Verification Method | Status |
|---|---|---|---|---|---|---|
| SWR-005 | POST /api/greet endpoint | HTTP routing | `backend/app/main.py:29-30`: `@app.post("/api/greet")` | `test_greet_success` | Assert HTTP 200, response contains greeting | Fully Traced |
| SWR-006 | API greeting satisfies core constraints | Endpoint logic + integration | `backend/app/main.py:33`: calls `hello(request.name)` | `test_greet_success` | Assert response format matches SWR-001 through SWR-004 | Fully Traced |
| SWR-007 | API input validation + 400 response | Error handling | `backend/app/main.py:35-36`: catch ValueError, raise HTTPException(400) | `test_greet_empty_name` | Assert HTTP 400, error detail in response | Fully Traced |
| SWR-008 | GET /health endpoint | HTTP routing | `backend/app/main.py:39-42`: `@app.get("/health")` | `test_health_check` | Assert HTTP 200, response is {"status": "ok"} | Fully Traced |

### SCI-003: Frontend UI

| Software Requirement | Description | Design Element | Implementation | Test | Verification Method | Status |
|---|---|---|---|---|---|---|
| SWR-009 | Form with input field and button | JSX form | `frontend/src/App.tsx:32-44`: `<form>`, `<input>`, `<button>` | Manual exploration | Open UI in browser, observe form elements | Fully Traced |
| SWR-010 | POST to /api/greet on submit | Form event handler + API client | `frontend/src/App.tsx:11-26`: `handleSubmit` calls `greet(name)` | Manual exploration | Submit form, observe network POST | Fully Traced |
| SWR-011 | Display greeting result | Result component | `frontend/src/App.tsx:46-49`: success result div | Manual exploration | Submit valid name, observe greeting displayed | Fully Traced |
| SWR-012 | Display error messages | Error component | `frontend/src/App.tsx:52-55`: error result div | Manual exploration | Submit empty name, observe error displayed | Fully Traced |
| SWR-013 | Loading state feedback | UI state management | `frontend/src/App.tsx:9, 15, 24, 39, 41-42`: loading state, disabled button | Manual exploration | Submit form, observe button text "Loading..." | Fully Traced |
| SWR-014 | Clear input after success | Form reset | `frontend/src/App.tsx:20`: `setName('')` after success | Manual exploration | Submit form, observe input cleared | Fully Traced |

## 4. Test Evidence Summary

### Unit Tests (SCI-001)

**File:** `tests/test_hello.py`  
**Execution:** Automated, CI pipeline  
**Framework:** Pytest  
**Count:** 4 tests  
**Status:** All pass  

| Test | Line | Requirement | Assertion |
|---|---|---|---|
| `test_greeting_contains_name` | 11-13 | REQ-001 / SWR-001 | `assert "Alice" in hello("Alice")` |
| `test_default_greeting` | 16-18 | REQ-002 / SWR-002 | `assert hello("Alice").startswith("Hello")` |
| `test_empty_name_is_rejected` | 21-24 | REQ-003 / SWR-003 | `with pytest.raises(ValueError)` |
| `test_greeting_ends_with_exclamation_mark` | 27-29 | REQ-004 / SWR-004 | `assert hello("Alice").endswith("!")` |

**Evidence:** Observed in CI pipeline output (GitHub Actions)

### Backend API Tests (SCI-002)

**File:** `backend/tests/test_main.py`  
**Execution:** Automated, CI pipeline  
**Framework:** Pytest + FastAPI TestClient  
**Count:** 3 tests  
**Status:** All pass  

| Test | Line | Requirement | Assertion |
|---|---|---|---|
| `test_greet_success` | 12-20 | REQ-006 / SWR-005, SWR-006 | Assert HTTP 200, response contains greeting, matches format |
| `test_greet_empty_name` | 23-28 | REQ-007 / SWR-007 | Assert HTTP 400, error detail present |
| `test_health_check` | 31-35 | REQ-006 / SWR-008 | Assert HTTP 200, response is `{"status": "ok"}` |

**Evidence:** Observed in CI pipeline output (GitHub Actions), test-results.xml artifact

### Backend Unit Tests (SCI-001 re-verified via backend)

**File:** `backend/tests/test_greeting.py`  
**Execution:** Automated, CI pipeline  
**Framework:** Pytest  
**Count:** 4 tests (same tests as original module, imported via backend)  
**Status:** All pass  

| Test | Line | Requirement | Purpose |
|---|---|---|---|
| `test_greeting_contains_name` | 8-10 | REQ-001 | Verify core module works from backend context |
| `test_default_greeting` | 13-15 | REQ-002 | Verify core module works from backend context |
| `test_empty_name_is_rejected` | 18-21 | REQ-003 | Verify core module works from backend context |
| `test_greeting_ends_with_exclamation_mark` | 24-26 | REQ-004 | Verify core module works from backend context |

**Evidence:** Observed in CI pipeline output (GitHub Actions)

### Frontend Tests (SCI-003)

**Type:** Manual exploratory testing  
**Scope:** REQ-008 / SWR-009 through SWR-014  
**Evidence:** Documented in `docs/requirements.md` section 4  

| Test Case | Requirement | Method |
|---|---|---|
| Enter valid name → greeting displayed | SWR-011 | Manual: open UI, enter "Alice", submit, observe greeting |
| Enter empty name → error displayed | SWR-012 | Manual: open UI, submit empty, observe error |
| Submit form → loading state visible | SWR-013 | Manual: open UI, submit, observe "Loading..." button text |
| After success → input cleared | SWR-014 | Manual: open UI, submit, observe input field cleared |
| Form elements present | SWR-009 | Manual: open UI, observe input field and button |
| Form submission → HTTP POST | SWR-010 | Manual: open browser DevTools, submit, observe POST in Network tab |

## 5. Coverage Analysis

### Requirements Implemented

| Requirement | Status | Traceability |
|---|---|---|
| REQ-001 | ✓ Implemented | SWR-001 → `src/hello.py:30` → `tests/test_hello.py:11-13` |
| REQ-002 | ✓ Implemented | SWR-002 → `src/hello.py:12` → `tests/test_hello.py:16-18` |
| REQ-003 | ✓ Implemented | SWR-003 → `src/hello.py:27-28` → `tests/test_hello.py:21-24` |
| REQ-004 | ✓ Implemented | SWR-004 → `src/hello.py:30` → `tests/test_hello.py:27-29` |
| REQ-005 | ✗ Not Implemented | SWR-015 → (unallocated) → (no test) |
| REQ-006 | ✓ Implemented | SWR-005 → `backend/app/main.py:29-36` → `backend/tests/test_main.py:12-20` |
| REQ-007 | ✓ Implemented | SWR-007 → `backend/app/main.py:35-36` → `backend/tests/test_main.py:23-28` |
| REQ-008 | ✓ Implemented | SWR-009-SWR-014 → `frontend/src/App.tsx` → Manual testing |

**Summary:**
- **Total Requirements:** 8
- **Implemented:** 7 (87.5%)
- **Not Implemented:** 1 (REQ-005 / Logging)
- **Fully Traced:** 7 of 7 implemented requirements

### Test Coverage

| Category | Count | Status |
|---|---|---|
| Automated Unit Tests (Core) | 4 | All pass |
| Automated Backend Unit Tests | 4 | All pass |
| Automated API Integration Tests | 3 | All pass |
| Manual Frontend Tests | 6 | All pass |
| **Total Tests** | **17** | **All pass** |
| **Unimplemented Requirement (REQ-005)** | 0 tests | N/A |

**Code Coverage Metrics (from CI pipeline):**

| Module | Coverage | Status |
|---|---|---|
| `src/hello.py` | 100% | EVIDENCE: CI pipeline reports coverage |
| `backend/app/` | Expected >90% | EVIDENCE: CI pipeline runs `--cov` |

## 6. Gap Analysis

### Design Gaps

| Requirement | Gap | Impact | Status |
|---|---|---|---|
| REQ-005 (Logging) | Not implemented | Logging unavailable for debugging | Design Gap — Intentional, documented |

**Classification:** MISSING — Unimplemented in v1.0.0 (documented as future enhancement)

### Verification Gaps

| Requirement | Gap | Impact | Recommendation |
|---|---|---|---|
| REQ-008 (Frontend UI) | No automated tests | Regression risk; incomplete verification | Add Vitest + Playwright for automated E2E testing |

**Classification:** Verification Gap — Manual testing only (acceptable for demonstration, risky for production)

### Other Observations

**No Conflicts Detected.**  
All requirements allocations are consistent; no contradictory implementations observed.

## 7. Traceability Metrics

| Metric | Value | Status |
|---|---|---|
| Requirements with full traceability chain | 7 / 7 implemented | ✓ Fully traced |
| Unimplemented requirements | 1 / 8 total | Design gap (REQ-005) |
| Tests without traceability to requirements | 0 | ✓ No orphaned tests |
| Requirements without tests | 1 | REQ-005 (unimplemented) |
| Fully traced implemented requirements | 7 / 7 | 100% |

**Overall Traceability:** 7 out of 7 implemented requirements are fully traced.

## 8. RTM Status and Review

**Status:** DRAFT  

**Verification:** ✓ Complete  
- All implemented requirements are mapped to software requirements
- All software requirements are mapped to design elements and code
- All code implementations are traced to automated or manual tests
- No orphaned code or tests detected
- No conflicting allocations

**Human Review Required Before Baseline:**
- [ ] Traceability chain confirmed accurate
- [ ] Test evidence verified
- [ ] REQ-005 gap accepted as design decision (intentional unimplemented)
- [ ] Frontend testing approach (manual only) acceptable for current phase
- [ ] RTM approved for baseline

---

**Document Generated By:** System Design QMS Assistant  
**Generation Date:** 2026-09-02  
**Authority:** VERIFIED requirements + EVIDENCE implementation  
**Classification:** DRAFT — Human review and approval required before traceability baseline
