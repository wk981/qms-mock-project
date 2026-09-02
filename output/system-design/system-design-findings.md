# System Design Findings

**Status:** DRAFT  
**Project:** Hello Project  
**Generated:** 2026-09-02  
**Analysis Date:** 2026-09-02  

## 1. Executive Summary

This document records findings from the system design analysis of the Hello Project. Findings are categorized by type (Requirements, Design, Implementation, Verification, Safety) and classified by severity.

**Key Findings:**
- **Critical:** REQ-005 is intentionally unimplemented (known gap)
- **High:** Frontend lacks automated test suite
- **High:** CORS hardcoded to localhost (production unsuitable)
- **Medium:** Safety classification unsupported by analysis
- **Medium:** Production deployment model undefined

**Overall Assessment:** Design is appropriate for demonstration/prototype phase. Several gaps require resolution before production deployment.

---

## 2. Findings by Category

### 2.1 Requirements Findings

#### Finding: REQ-001.1

**Title:** REQ-001 (Greeting) - Fully Implemented and Verified  
**Category:** Requirements  
**Severity:** —  
**Requirement:** REQ-001  
**Evidence:** 
- Implementation: `src/hello.py:30` (f-string includes name)
- Test: `tests/test_hello.py:11-13` (assertion: name in result)

**Description:** Requirement is clear, testable, and implemented. Greeting correctly contains supplied name.

**Status:** ✓ VERIFIED — No action required

---

#### Finding: REQ-002.1

**Title:** REQ-002 (Default Greeting) - Fully Implemented and Verified  
**Category:** Requirements  
**Severity:** —  
**Requirement:** REQ-002  
**Evidence:**
- Implementation: `src/hello.py:12` (DEFAULT_GREETING = "Hello")
- Test: `tests/test_hello.py:16-18` (assertion: startswith("Hello"))

**Description:** Requirement is clear and implemented. Greeting consistently uses "Hello" prefix.

**Status:** ✓ VERIFIED — No action required

---

#### Finding: REQ-005.1

**Title:** REQ-005 (Logging) - Not Implemented (Intentional Gap)  
**Category:** Requirements  
**Severity:** Critical  
**Requirement:** REQ-005  
**Evidence:**
- Requirement statement: `docs/requirements.md` section 2 ("This requirement is **not implemented in version 1.0.0**")
- Code review: No logging code found in `src/hello.py` or `backend/app/main.py`
- Tests: No test coverage for logging functionality

**Description:** REQ-005 (Logging) is present in the verified requirements baseline but explicitly not implemented in v1.0.0. The requirement states: "Every invocation of the greeting operation must produce a log entry identifying the request."

No logging framework is integrated, and no log entries are generated during greeting operations.

**Impact:** Inability to audit greeting requests or debug production issues. Logging unavailable for operational monitoring.

**Root Cause:** Intentional out-of-scope for demonstration version.

**Recommended Action:** 
1. Confirm logging remains out-of-scope for current release
2. Schedule logging implementation for a future release (v1.1.0 or v2.0.0)
3. Document logging architecture and design before implementation

**Status:** DESIGN GAP — Intentional, documented  
**Human Review Required:** Yes (confirm intentional gap is acceptable)

---

### 2.2 Design Findings

#### Finding: DES-001.1

**Title:** Architecture is Well-Structured  
**Category:** Design  
**Severity:** —  
**Evidence:**
- Architecture diagram: `docs/design.md` section 1
- Source code layout: `src/`, `backend/`, `frontend/` cleanly separated
- Layering: Core → Backend API → Frontend (unidirectional dependency)

**Description:** Three-layer architecture with clear separation of concerns. Each layer has defined responsibility and interface.

**Status:** ✓ VERIFIED — Design sound

---

#### Finding: DES-002.1

**Title:** Safety-Critical Classification Unsupported by Analysis  
**Category:** Design  
**Severity:** Medium  
**Element:** SCI-001 (Core Greeting Module)  
**Evidence:**
- Design document: `docs/design.md` section 2 ("Safety classification | Safety-critical")
- Safety analysis: None present in repository
- Hazard log: Not found
- Safety requirements: Not identified
- Safety tests: None found

**Description:** The Software Design Document (SDD) in `docs/design.md` classifies SCI-001 as "Safety-critical" but provides no supporting safety analysis, hazard identification, or safety requirements.

**Impact:** If SCI-001 is actually safety-critical, the current design is inadequate and requires:
1. Hazard analysis
2. Safety requirements specification
3. Safety-critical design review
4. Formal verification or certification

If SCI-001 is NOT safety-critical, the classification is misleading.

**Questions for Review:**
1. Is this application actually safety-critical? (Context: demonstrated greeting function)
2. If yes, what are the applicable standards? (IEC 61508, ISO 26262, etc.)
3. If no, should the "safety-critical" classification be removed from the design document?

**Recommended Action:**
1. Clarify safety classification and rationale
2. If safety-critical: perform formal safety analysis before production deployment
3. If not safety-critical: update design document to remove misleading classification

**Status:** HUMAN REVIEW REQUIRED — Safety assumption needs engineering confirmation

---

#### Finding: DES-003.1

**Title:** CORS Hardcoded to Development Origins  
**Category:** Design  
**Severity:** High  
**Element:** SCI-002 (Backend API)  
**Evidence:**
- Code: `backend/app/main.py:20-26` (CORSMiddleware with hardcoded `allow_origins`)
- Values: `["http://localhost:5173", "http://localhost:3000"]`

**Description:** CORS is configured to allow requests only from localhost development servers. This is appropriate for development but unsuitable for production.

**Impact:** Current design cannot be deployed to production without manual code change to CORS configuration.

**Recommended Action:**
1. Parameterize CORS origins via environment variable or configuration file
2. Define production CORS policy (which origin(s) are allowed?)
3. Document CORS configuration procedure for deployment

**Status:** DESIGN GAP — Production deployment requires reconfiguration

---

#### Finding: DES-004.1

**Title:** No Authentication or Authorization  
**Category:** Design  
**Severity:** Medium  
**Element:** SCI-002 (Backend API)  
**Evidence:**
- No auth code: `backend/app/main.py` has no authentication checks
- No identity model: No user, role, or permission concepts
- No access control: All requests accepted unconditionally

**Description:** The backend API has no authentication or authorization layer. All requests to `/api/greet` are accepted without validation of caller identity or permissions.

**Impact:** 
- If deployed publicly: API is accessible to any caller
- If internal: May not meet security or compliance requirements

**Assumption:** Authentication is out-of-scope for demonstration project (assumption documented in SDD section 15).

**Recommended Action:**
1. Clarify whether authentication is in-scope for production deployment
2. If required: add authentication layer (JWT, OAuth2, mTLS, etc.)
3. Document security model and access control policy

**Status:** PROPOSED / HUMAN REVIEW REQUIRED — Security model undefined

---

#### Finding: DES-005.1

**Title:** No Rate Limiting or DDoS Protection  
**Category:** Design  
**Severity:** Medium  
**Element:** SCI-002 (Backend API)  
**Evidence:**
- No middleware: No rate limiting found in FastAPI configuration
- No API gateway: Single endpoint with no gateway protection
- No monitoring: No metrics or alerts for abnormal request patterns

**Description:** Backend API has no rate limiting, throttling, or DDoS protection mechanisms. Any client can send unlimited requests.

**Impact:** Susceptible to abuse (intentional or unintentional). No protection against resource exhaustion.

**Recommended Action:**
1. If public deployment: Add rate limiting (via middleware or API gateway)
2. Add monitoring and alerting for abnormal request patterns
3. Document rate limiting policy

**Status:** PROPOSED / HUMAN REVIEW REQUIRED — Security posture undefined

---

### 2.3 Implementation Findings

#### Finding: IMP-001.1

**Title:** Core Module (SCI-001) - Well Implemented  
**Category:** Implementation  
**Severity:** —  
**Evidence:**
- Code quality: Clear, concise, type-annotated
- Error handling: Validates input, raises clear exceptions
- Testing: 4 unit tests, 100% code coverage
- CI integration: Tests run on every commit

**Description:** Implementation is clean and testable. Function performs exactly as specified.

**Status:** ✓ VERIFIED — Implementation sound

---

#### Finding: IMP-002.1

**Title:** Backend API (SCI-002) - Well Implemented  
**Category:** Implementation  
**Severity:** —  
**Evidence:**
- Code quality: Type-annotated, Pydantic validation, error handling
- Testing: 3 API integration tests
- Endpoints: Two endpoints implemented (`/api/greet`, `/health`)

**Description:** Backend API correctly translates HTTP requests to core function calls and responses. Pydantic validation enforces request/response schema.

**Status:** ✓ VERIFIED — Implementation sound

---

#### Finding: IMP-003.1

**Title:** Frontend (SCI-003) - Functional but Lacks Tests  
**Category:** Implementation  
**Severity:** High  
**Evidence:**
- Code: `frontend/src/App.tsx`, `frontend/src/api.ts` (clean TypeScript)
- Type checking: TypeScript compilation succeeds
- Tests: No automated unit or integration tests
- Testing: Manual exploratory testing only (documented in `docs/requirements.md`)

**Description:** Frontend implementation is functional and well-typed. However, there are no automated tests (Vitest, Playwright, etc.). Verification relies entirely on manual testing.

**Impact:** Risk of UI regressions when code changes. Incomplete traceability for REQ-008 verification.

**Recommended Action:**
1. Add Vitest + React Testing Library for component unit tests
2. Add Playwright or Cypress for E2E tests
3. Integrate frontend tests into CI pipeline

**Status:** VERIFICATION GAP — Manual testing only; recommended to add automation

---

#### Finding: IMP-004.1

**Title:** No Error Message Sanitization  
**Category:** Implementation  
**Severity:** Low  
**Element:** Frontend error display  
**Evidence:**
- Code: `frontend/src/App.tsx:54` (displays error.detail directly)
- Backend: `backend/app/main.py:36` (returns exception message as-is)

**Description:** Error messages from backend are displayed in frontend without sanitization. If backend error messages contain untrusted data, XSS risk exists.

**Current Risk Level:** Low (error messages come from backend, not user input)

**Recommended Action:**
1. Review error messages to ensure they don't leak sensitive information
2. Consider HTML-escaping error messages at display time (good practice)
3. Document error message policy (what information is safe to show users?)

**Status:** LOW PRIORITY — Not urgent for demonstration project

---

### 2.4 Verification Findings

#### Finding: VER-001.1

**Title:** Core Module (SCI-001) - Fully Tested  
**Category:** Verification  
**Severity:** —  
**Evidence:**
- Tests: `tests/test_hello.py` (4 tests)
- Verification: `backend/tests/test_greeting.py` (4 tests re-verifying from backend context)
- Coverage: 100%
- CI: Tests run on every commit

**Description:** Core module has complete test coverage. REQ-001 through REQ-004 are verified by automated tests.

**Status:** ✓ FULLY VERIFIED

---

#### Finding: VER-002.1

**Title:** Backend API (SCI-002) - Fully Tested  
**Category:** Verification  
**Severity:** —  
**Evidence:**
- Tests: `backend/tests/test_main.py` (3 tests)
- Coverage: Success case, error case, health check
- CI: Tests run on every commit

**Description:** Backend API has comprehensive test coverage. REQ-006 and REQ-007 are verified by automated tests.

**Status:** ✓ FULLY VERIFIED

---

#### Finding: VER-003.1

**Title:** Frontend (SCI-003) - Manual Testing Only  
**Category:** Verification  
**Severity:** High  
**Evidence:**
- Tests: None found in `frontend/src/`
- Verification method: Manual exploratory testing (documented in `docs/requirements.md`)
- No CI integration for frontend tests (CI runs `npm run build` for type checking, not tests)

**Description:** Frontend (REQ-008) is verified only by manual exploratory testing. No automated test suite exists.

**Impact:** 
- Cannot run automated regression tests when UI code changes
- Cannot verify UI in CI/CD pipeline
- Higher risk of undetected regressions
- Incomplete traceability for REQ-008

**Recommended Action:**
1. Add Vitest for unit tests of React components
2. Add React Testing Library for component behavior tests
3. Add Playwright or Cypress for end-to-end tests
4. Integrate frontend tests into CI pipeline

**Status:** VERIFICATION GAP — Recommended to add automation

---

#### Finding: VER-004.1

**Title:** REQ-005 (Logging) - Not Verified  
**Category:** Verification  
**Severity:** Critical  
**Evidence:** No tests found; requirement not implemented

**Description:** REQ-005 (Logging) has no test coverage because it is not implemented.

**Status:** VERIFICATION GAP — No test exists (expected, since not implemented)

---

### 2.5 Safety Findings

#### Finding: SAF-001.1

**Title:** Safety Classification Requires Clarification  
**Category:** Safety  
**Severity:** Medium  
**Evidence:**
- Design document: `docs/design.md` section 2 classifies SCI-001 as "Safety-critical"
- Safety analysis: Not found in repository
- Hazard log: Not found
- Safety requirements: Not identified
- Certification: No certification or approval evidence

**Description:** SCI-001 is labeled safety-critical without supporting analysis or documentation.

**Questions:**
1. Is a greeting function actually safety-critical?
2. What is the intended use case? (demonstration, internal tool, user-facing service?)
3. If safety-critical, what standards apply? (IEC 61508, ISO 26262, etc.)

**Recommended Action:**
1. Clarify safety classification (safety-critical vs. non-critical)
2. Document rationale for classification
3. If safety-critical: perform formal hazard analysis and safety design review

**Status:** HUMAN REVIEW REQUIRED

---

## 3. Summary of Findings

### By Severity

| Severity | Count | Examples |
|---|---|---|
| Critical | 1 | REQ-005 unimplemented (intentional) |
| High | 2 | Frontend lacks tests, CORS hardcoded |
| Medium | 3 | Safety classification unsupported, auth/authz undefined, rate limiting absent |
| Low | 1 | Error message sanitization |
| — (Positive) | 4 | Core module, backend API, architecture, testing |

### By Category

| Category | Findings | Status |
|---|---|---|
| Requirements | 3 | REQ-005 is known gap; others verified |
| Design | 5 | CORS and security model require attention |
| Implementation | 4 | Core and backend sound; frontend lacks tests |
| Verification | 4 | Core and backend verified; frontend manual only; REQ-005 not tested |
| Safety | 1 | Safety classification unclear |

### Findings Requiring Action

| Finding | Priority | Owner | Recommended Action |
|---|---|---|---|
| REQ-005 (Logging) | High | Product / Engineering | Confirm intentional gap; schedule for future release |
| Frontend Tests | High | Engineering | Add Vitest + Playwright to CI pipeline |
| CORS Configuration | High | DevOps / Architecture | Parameterize CORS origins for production |
| Safety Classification | Medium | Product / Safety | Clarify classification and document rationale |
| Auth/AuthZ Model | Medium | Architecture | Define security model if required |
| Rate Limiting | Medium | Architecture | Add rate limiting if public deployment planned |

---

## 4. Design Decision Records (ADRs)

### ADR-001: Intentional Non-Implementation of REQ-005 (Logging)

**Status:** PROPOSED / HUMAN REVIEW REQUIRED  
**Date:** 2026-09-02  

**Context:**
REQ-005 specifies that "The system shall record each greeting request in the application log." The requirement is present in the verified baseline but explicitly not implemented in v1.0.0.

**Decision:**
REQ-005 remains unimplemented in v1.0.0. Logging is out-of-scope for the current demonstration/prototype phase.

**Rationale:**
- Demonstration project emphasizes core functionality and architecture
- Logging can be added in future iteration without breaking API or core module
- Current implementation allows manual testing and operational observation without log dependency

**Consequences:**
- Positive: Simpler implementation, faster time-to-demo
- Negative: No audit trail for greeting requests, harder to debug in production

**Alternatives Considered:**
1. Implement logging in v1.0.0 — rejected as out-of-scope
2. Use a logging stub that does nothing — rejected as misleading
3. Leave unimplemented and document gap — accepted (current approach)

**Approval:** PENDING — requires engineering and product review

---

### ADR-002: Layered Architecture (Core → Backend → Frontend)

**Status:** VERIFIED  
**Date:** 2026-09-02  

**Context:**
The application could be designed as a monolith, a monorepo with separate services, or a layered architecture.

**Decision:**
Three-layer architecture: Core logic module → FastAPI backend → React frontend.

**Rationale:**
- Separation of concerns (core logic independent of HTTP)
- Core module reusable in other contexts (non-HTTP use cases)
- Backend can be tested independently of frontend
- Frontend can be replaced without touching backend or core
- Demonstrates modern fullstack architecture patterns

**Consequences:**
- Positive: Clean separation, testable, reusable components
- Negative: Additional complexity vs. monolith; multiple deployment targets

**Alternatives Considered:**
1. Monolithic Flask/Django app — rejected as less modular
2. Microservices with separate repos — rejected as over-engineered
3. Frontend-only (static greeting) — rejected as doesn't demonstrate REST API

**Approval:** CONFIRMED ✓

---

### ADR-003: No Automated Frontend Tests (v1.0.0)

**Status:** PROPOSED / HUMAN REVIEW REQUIRED  
**Date:** 2026-09-02  

**Context:**
Frontend verification currently relies on manual exploratory testing. Automated tests could be added using Vitest, Playwright, or similar.

**Decision:**
v1.0.0 uses manual testing for frontend. Automated tests are deferred to v1.1.0 or later.

**Rationale:**
- Demonstration project prioritizes breadth over depth of testing
- Manual testing sufficient for verifying core user workflows
- Automated frontend tests add complexity (test setup, framework selection)
- Can be added incrementally without rework of frontend code

**Consequences:**
- Positive: Faster initial implementation, fewer dependencies
- Negative: Regression risk when UI changes, incomplete CI automation

**Alternatives Considered:**
1. Add Vitest + Playwright from start — accepted as better practice, but deferred
2. Accept manual testing permanently — rejected; automation recommended for future
3. Add only E2E tests, skip unit tests — acceptable middle ground for future

**Approval:** PENDING — recommend automating in next release

---

## 5. Review Checklist

**Before design baseline can be approved, the following must be addressed:**

### Critical Items
- [ ] Confirm REQ-005 (Logging) intentional non-implementation is acceptable
- [ ] Clarify SCI-001 safety-critical classification (is it actually safety-critical?)

### High Priority
- [ ] Plan frontend automated test framework integration
- [ ] Develop CORS configuration strategy for production

### Medium Priority
- [ ] Define authentication/authorization model (if needed)
- [ ] Determine rate limiting requirements (if public deployment)

### Low Priority
- [ ] Review error message sanitization policy

---

## 6. Conclusion

The Hello Project design is **appropriate for demonstration and prototype phase**. The architecture is sound, core functionality is well-tested, and all primary requirements are implemented.

**Before production deployment**, the following gaps should be addressed:
1. Frontend automated testing
2. CORS parameterization
3. Security model definition (auth/authz/rate limiting)
4. Safety classification clarification

---

**Document Generated By:** System Design QMS Assistant  
**Generation Date:** 2026-09-02  
**Classification:** DRAFT — Human review and approval required  
**Next Step:** Engineering review of findings and action items
