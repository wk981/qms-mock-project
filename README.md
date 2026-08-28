# Hello Project

## Project

Hello Project

## Purpose

This is a demonstration software project for automated **Development, Test and Evaluation
(DTE)** documentation generation.

The software itself is deliberately trivial — a single greeting function that any engineer
can understand in a couple of minutes. The value of this repository lies in the
engineering evidence built around that software: a requirements specification, a design
document, source code, unit tests, issue-tracked development work, a git history, and a
continuous integration pipeline that emits machine-readable test and build evidence.

That evidence is the input to a separate DTE documentation process, which consumes this
repository and produces the DTE output documents. Those output documents are **not**
contained in this repository.

## Repository

`hello-project`

## Version

`1.0.0`

## Safety Classification

The `hello` module is classified as safety-critical for this demonstration project.

Because the module is safety-critical, **Unit Test Results documentation is applicable**
to it under the DTE process.

## Requirements

The software requirements are specified in [`docs/requirements.md`](docs/requirements.md).

| Requirement | Title | Implemented in v1.0.0 |
|---|---|---|
| REQ-001 | Greeting | Yes |
| REQ-002 | Default Greeting | Yes |
| REQ-003 | Input Validation | Yes |
| REQ-004 | Punctuation | Yes |
| REQ-005 | Logging | **No** |

REQ-005 is not implemented in version 1.0.0. It has no implementation, no unit test and no
CI verification evidence.

## Design

The software design is described in [`docs/design.md`](docs/design.md).

The design defines one software configuration item:

* **SCI-001 — `src/hello.py`** — responsible for generating greetings and validating input.

## Usage

```python
from src.hello import hello

hello("Alice")   # "Hello, Alice!"
hello("")        # raises ValueError: Name cannot be empty
```

## Testing

The unit tests live in [`tests/test_hello.py`](tests/test_hello.py) and are written with
pytest. Each test verifies a single requirement and its docstring names that requirement.

| Test | Requirement |
|---|---|
| `test_greeting_contains_name` | REQ-001 |
| `test_default_greeting` | REQ-002 |
| `test_empty_name_is_rejected` | REQ-003 |
| `test_greeting_ends_with_exclamation_mark` | REQ-004 |

To run the tests locally:

```bash
pip install pytest pytest-cov
pytest --junitxml=test-results.xml --cov=src --cov-report=xml:coverage.xml
```

## Continuous Integration

GitHub Actions runs the automated tests on every push and pull request and produces
machine-readable artifacts. The workflow is defined in
[`.github/workflows/ci.yml`](.github/workflows/ci.yml).

The CI pipeline produces the following evidence, uploaded as the **`dte-evidence`**
artifact on every run:

| File | Format | Contents |
|---|---|---|
| `test-results.xml` | JUnit XML | Unit test results — total, passed, failed, skipped, and individual test names |
| `coverage.xml` | Cobertura XML | Code coverage results for `src/` |
| `build-info.json` | JSON | Build information |

`build-info.json` has the following shape. The commit SHA and build number are taken from
the GitHub Actions environment at run time and are never hard-coded:

```json
{
  "project": "Hello Project",
  "repository": "hello-project",
  "version": "1.0.0",
  "commit": "<GITHUB_SHA>",
  "build_number": "<GITHUB_RUN_NUMBER>",
  "status": "passed"
}
```

The latest CI result for any commit can be found on the
[Actions](../../actions) tab, and the evidence artifact can be downloaded from the
corresponding run.

## Repository layout

```text
hello-project/
├── README.md
├── pytest.ini
├── docs/
│   ├── requirements.md          Software Requirements Specification
│   └── design.md                Software Design Document
├── src/
│   ├── __init__.py
│   └── hello.py                 SCI-001
├── tests/
│   ├── __init__.py
│   └── test_hello.py            Unit tests for SCI-001
├── .github/
│   └── workflows/
│       └── ci.yml               CI pipeline and evidence generation
└── output/                      Reserved for generated DTE documents
```

## Development history

The development work is tracked in the repository's GitHub Issues, each of which
references the requirement it implements, and in the git history. Version `1.0.0` is
tagged as `v1.0.0`.
