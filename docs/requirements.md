# Software Requirements Specification

| Field | Value |
|---|---|
| Project | Hello Project |
| Repository | `hello-project` |
| Version | 1.0.0 |
| Status | Approved |

## 1. Introduction

This document specifies the software requirements for the Hello Project demonstration
application. The application provides a single greeting operation.

Each requirement is uniquely identified and is written so that it can be verified by a
unit test.

## 2. Requirements

### REQ-001 — Greeting

The system shall return a greeting containing the supplied name.

Given a name such as `Alice`, the greeting returned by the system must include the
string `Alice`.

### REQ-002 — Default Greeting

The system shall use "Hello" as the default greeting.

The greeting returned by the system must begin with the word `Hello`.

### REQ-003 — Input Validation

The system shall reject an empty name.

If the supplied name is empty, the system must not return a greeting and must instead
signal an input validation error.

### REQ-004 — Punctuation

The greeting shall end with an exclamation mark.

The final character of the greeting returned by the system must be `!`.

### REQ-005 — Logging

The system shall record each greeting request in the application log.

Every invocation of the greeting operation must produce a log entry identifying the
request. This requirement is **not implemented in version 1.0.0**.

### REQ-006 — Greeting API

The system shall expose the greeting operation over HTTP via a REST API.

The API shall accept POST requests to `/api/greet` with a JSON body containing a `name`
field, and return a JSON response containing the greeting. The returned greeting must
satisfy REQ-001 through REQ-004.

### REQ-007 — API Input Validation

The system shall validate input at the API boundary and reject empty names with an
appropriate HTTP error response.

When an empty or missing name is supplied via the `/api/greet` endpoint, the system
must return an HTTP 400 response with an error detail message, rather than returning a
greeting.

### REQ-008 — Greeting Web Interface

The system shall provide a web-based user interface for submitting a name and viewing
the resulting greeting.

A user shall be able to open the web UI in a browser, enter their name in a form,
submit the form, and see the greeting or an error message displayed on the page.

## 3. Requirement Status

| Requirement | Title | Status |
|---|---|---|
| REQ-001 | Greeting | Implemented |
| REQ-002 | Default Greeting | Implemented |
| REQ-003 | Input Validation | Implemented |
| REQ-004 | Punctuation | Implemented |
| REQ-005 | Logging | Not implemented |
| REQ-006 | Greeting API | Implemented |
| REQ-007 | API Input Validation | Implemented |
| REQ-008 | Greeting Web Interface | Implemented |

## 4. Verification

Requirements REQ-001 through REQ-004 are verified by the automated unit tests in
`tests/test_hello.py` and `backend/tests/test_greeting.py`, which are executed by
the continuous integration pipeline on every push and pull request.

REQ-005 has no implementation and no verification; it is a known gap.

Requirements REQ-006 and REQ-007 are verified by the API integration tests in
`backend/tests/test_main.py`, which test the `/api/greet` endpoint with both valid
and invalid input.

Requirement REQ-008 is verified by manual exploratory testing of the web interface
at `http://localhost:5173` (development) or the production deployment URL.
