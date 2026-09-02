# Software Design Document

| Field | Value |
|---|---|
| Project | Hello Project |
| Repository | `hello-project` |
| Version | 1.0.0 |
| Related document | [Software Requirements Specification](requirements.md) |

## 1. Architecture

The demonstration application consists of a single small Python module.

There is no database, no network service and no user interface. A caller imports the
module and invokes one function.

```text
caller
  │
  ▼
src/hello.py  ──►  hello(name) ──► greeting string
                        │
                        └────────► ValueError (invalid input)
```

The module is pure and stateless: the same input always produces the same output, and no
state is retained between calls. This keeps the module fully testable by unit test alone.

## 2. Software Configuration Items

### SCI-001 — `hello.py`

Location: `src/hello.py`

This module is responsible for:

* **generating greetings** — constructing the greeting text from the supplied name
* **validating input** — rejecting an empty name before a greeting is constructed

| Attribute | Value |
|---|---|
| Configuration item | SCI-001 |
| File | `src/hello.py` |
| Language | Python 3 |
| Safety classification | Safety-critical (see README) |
| Requirements allocated | REQ-001, REQ-002, REQ-003, REQ-004 |
| Unit tests | `tests/test_hello.py` |

## 3. Interface

```text
hello(name: str) -> str
```

**Input**

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | The name to greet. Must be a non-empty string. |

**Output**

A greeting string of the form `Hello, <name>!`.

The returned string begins with the default greeting `Hello` (REQ-002), contains the
supplied name (REQ-001), and ends with an exclamation mark (REQ-004).

**Example**

```text
hello("Alice")  ->  "Hello, Alice!"
```

## 4. Error Handling

An empty name results in a `ValueError`.

| Condition | Behaviour |
|---|---|
| `name` is empty | Raise `ValueError("Name cannot be empty")` |

The validation check is performed before the greeting is constructed, so no greeting is
returned when the input is invalid. This implements REQ-003.

No other error conditions are handled; any other input is passed through to string
formatting unchanged.

## 5. Design Limitations

Version 1.0.0 implements REQ-001 through REQ-004 only.

REQ-005 (Logging) is not addressed by this design. The module performs no logging, and no
logging component is defined.
