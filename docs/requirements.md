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

## 3. Requirement Status

| Requirement | Title | Status in v1.0.0 |
|---|---|---|
| REQ-001 | Greeting | Implemented |
| REQ-002 | Default Greeting | Implemented |
| REQ-003 | Input Validation | Implemented |
| REQ-004 | Punctuation | Implemented |
| REQ-005 | Logging | Not implemented |

## 4. Verification

Requirements REQ-001 through REQ-004 are verified by the automated unit tests in
`tests/test_hello.py`, which are executed by the continuous integration pipeline on
every push and pull request.

REQ-005 has no implementation and no verification in version 1.0.0.
