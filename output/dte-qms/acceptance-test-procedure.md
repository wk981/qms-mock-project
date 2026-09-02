# Acceptance Test Procedure

**Status:** DRAFT  
**Project:** Hello Project  
**Generated:** 2026-09-02  
**Baseline:** System Requirements (REQ-001 through REQ-008)  

## 1. Purpose

This document defines acceptance test procedures for verifying that the Hello Project meets its system requirements. Each requirement is associated with one or more test cases that, when executed and passing, provide evidence of requirement satisfaction.

## 2. Test Scope

**Requirements Tested:** REQ-001 through REQ-008  
**Out of Scope:** REQ-005 (Logging) — not implemented in v1.0.0  

**Test Categories:**
- Unit acceptance tests (core module behavior)
- API acceptance tests (HTTP endpoint behavior)
- Functional acceptance tests (end-to-end user workflows)

## 3. Acceptance Test Matrix

### REQ-001: Greeting Contains Name

| Test ID | Title | Test Case | Acceptance Criteria |
|---|---|---|---|
| ATP-001 | Greeting includes supplied name | Call `hello("Alice")` | Result contains "Alice" |

**Procedure:**
1. Invoke the greeting function with name "Alice"
2. Capture the returned greeting string
3. Verify string contains "Alice"

**Pass Criteria:** String contains the supplied name

---

### REQ-002: Default Greeting Prefix

| Test ID | Title | Test Case | Acceptance Criteria |
|---|---|---|---|
| ATP-002 | Greeting begins with "Hello" | Call `hello("Alice")` | Result starts with "Hello" |

**Procedure:**
1. Invoke the greeting function with name "Alice"
2. Capture the returned greeting string
3. Verify string begins with "Hello"

**Pass Criteria:** Greeting starts with "Hello"

---

### REQ-003: Input Validation — Empty Name Rejection

| Test ID | Title | Test Case | Acceptance Criteria |
|---|---|---|---|
| ATP-003 | Empty name raises error | Call `hello("")` | ValueError raised |

**Procedure:**
1. Invoke the greeting function with empty string ""
2. Observe if an exception is raised
3. Verify exception type is ValueError
4. Verify exception message indicates name validation failure

**Pass Criteria:** ValueError is raised; message indicates name validation

---

### REQ-004: Punctuation — Exclamation Mark

| Test ID | Title | Test Case | Acceptance Criteria |
|---|---|---|---|
| ATP-004 | Greeting ends with "!" | Call `hello("Alice")` | Result ends with "!" |

**Procedure:**
1. Invoke the greeting function with name "Alice"
2. Capture the returned greeting string
3. Verify string ends with "!"

**Pass Criteria:** Greeting ends with exclamation mark

---

### REQ-006: Greeting API over HTTP

| Test ID | Title | Test Case | Acceptance Criteria |
|---|---|---|---|
| ATP-005 | POST /api/greet endpoint exists | POST to `/api/greet` with `{"name": "Alice"}` | HTTP 200 response with greeting JSON |

**Procedure:**
1. Start the backend service (FastAPI on localhost:8000)
2. Send HTTP POST request to `http://localhost:8000/api/greet`
3. Include JSON body: `{"name": "Alice"}`
4. Capture HTTP status code and response body
5. Verify status code is 200
6. Verify response body contains JSON with "greeting" field
7. Verify greeting value matches REQ-001 through REQ-004 constraints

**Pass Criteria:** 
- HTTP 200 response
- Response JSON contains "greeting" field
- Greeting satisfies REQ-001, REQ-002, REQ-004

---

### REQ-007: API Input Validation

| Test ID | Title | Test Case | Acceptance Criteria |
|---|---|---|---|
| ATP-006 | Empty name returns HTTP 400 | POST to `/api/greet` with `{"name": ""}` | HTTP 400 response with error detail |

**Procedure:**
1. Start the backend service (FastAPI on localhost:8000)
2. Send HTTP POST request to `http://localhost:8000/api/greet`
3. Include JSON body: `{"name": ""}`
4. Capture HTTP status code and response body
5. Verify status code is 400 (Bad Request)
6. Verify response JSON contains "detail" field with error message

**Pass Criteria:**
- HTTP 400 response
- Response contains error detail message
- Detail message indicates name validation failure

---

### REQ-008: Web-Based User Interface

| Test ID | Title | Test Case | Acceptance Criteria |
|---|---|---|---|
| ATP-007 | Frontend form displays | Open frontend in browser | Form with input field and submit button visible |
| ATP-008 | Submit valid name | Enter "Alice" in form, submit | Greeting displayed in result area |
| ATP-009 | Submit empty name | Leave input empty, submit | Error message displayed |
| ATP-010 | Loading state visible | Submit form, observe during request | Button shows "Loading..." or disabled state |
| ATP-011 | Input cleared after success | Submit valid name | Input field cleared after greeting displayed |

**Procedure for ATP-007:**
1. Start frontend dev server (Vite on localhost:5173)
2. Start backend service (FastAPI on localhost:8000)
3. Open browser to `http://localhost:5173`
4. Observe page content

**Pass Criteria:**
- Page loads successfully
- Form element visible
- Input field with placeholder "Enter your name" present
- Submit button labeled "Get Greeting" or similar present

**Procedure for ATP-008:**
1. Setup: Frontend and backend running
2. Open frontend in browser
3. Type "Alice" in name input field
4. Click submit button
5. Observe result area

**Pass Criteria:**
- No error displayed
- Greeting displayed (e.g., "Hello, Alice!")
- Greeting satisfies REQ-001, REQ-002, REQ-004

**Procedure for ATP-009:**
1. Setup: Frontend and backend running
2. Open frontend in browser
3. Leave input field empty
4. Click submit button
5. Observe result area

**Pass Criteria:**
- Error message displayed (e.g., "Error: Name cannot be empty")

**Procedure for ATP-010:**
1. Setup: Frontend and backend running
2. Open frontend in browser
3. Type name in input field
4. Click submit button
5. Observe button during request

**Pass Criteria:**
- Button disabled or text changes to "Loading..."
- Feedback visible to user during request

**Procedure for ATP-011:**
1. Setup: Frontend and backend running
2. Open frontend in browser
3. Type name in input field
4. Click submit button
5. After greeting displayed, observe input field

**Pass Criteria:**
- Input field is empty after successful submission

---

## 4. Test Execution Environment

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Expected:** Backend listening on http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

**Expected:** Frontend available on http://localhost:5173

### Test Execution Method

| Test Type | Method | Invocation |
|---|---|---|
| ATP-001, ATP-002, ATP-003, ATP-004 | Automated unit test | `pytest tests/test_hello.py -v` |
| ATP-005, ATP-006 | Automated API test | `pytest backend/tests/test_main.py -v` |
| ATP-007 through ATP-011 | Manual exploratory test | Open browser, interact with form |

---

## 5. Acceptance Criteria Summary

| Requirement | Test Cases | Success Criteria |
|---|---|---|
| REQ-001 | ATP-001 | Greeting contains supplied name |
| REQ-002 | ATP-002 | Greeting begins with "Hello" |
| REQ-003 | ATP-003 | ValueError raised for empty name |
| REQ-004 | ATP-004 | Greeting ends with "!" |
| REQ-006 | ATP-005 | HTTP 200 with greeting JSON |
| REQ-007 | ATP-006 | HTTP 400 with error detail |
| REQ-008 | ATP-007 through ATP-011 | Form, interaction, feedback all present |

---

## 6. Test Data

### Valid Test Cases

| Input | Expected Greeting | Notes |
|---|---|---|
| "Alice" | "Hello, Alice!" | Basic case |
| "Bob" | "Hello, Bob!" | Different name |
| "J" | "Hello, J!" | Single character |
| "Alice Smith" | "Hello, Alice Smith!" | Multi-word name |

### Invalid Test Cases

| Input | Expected Behavior | Notes |
|---|---|---|
| "" | ValueError or HTTP 400 | Empty string |
| (missing field) | HTTP 400 | Missing name field in API request |

---

## 7. Test Pass/Fail Criteria

**Overall Acceptance:** All test cases must pass.

**Passing Test:** 
- Automated test: test completes without assertion failures
- Manual test: all acceptance criteria met, observed behavior matches expected behavior

**Failing Test:**
- Automated test: assertion fails or exception thrown
- Manual test: any acceptance criterion not met, or unexpected error observed

---

## 8. Notes

- REQ-005 (Logging) is not included in acceptance testing as it is not implemented in v1.0.0
- Frontend tests (ATP-007 through ATP-011) are manual; automated E2E testing recommended for future versions
- Test procedures assume clean environment (no prior state affecting results)

---

**Document Status:** DRAFT — Procedures defined; execution results recorded separately in Functional Test Results and Unit Test Results documents

**Next Steps:** Execute procedures; record results in test result documents
