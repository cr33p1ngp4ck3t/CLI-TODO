<!--
SYNC IMPACT REPORT
================================================================================
Version change: 1.1.0 → 1.2.0
Bump rationale: MINOR - Added feature tiers, monorepo structure, updated tech stack

Modified Principles:
- Principle IV: Technology Constraints - Python 3.13+, UV, Better Auth, cloud options
- NEW Principle VI: Feature Tiers - Basic/Intermediate/Advanced feature classification
- NEW Principle VII: Monorepo Structure - Required folder organization for Phase II+

Templates Status:
- .specify/templates/plan-template.md: ✅ Compatible
- .specify/templates/spec-template.md: ✅ Compatible
- .specify/templates/tasks-template.md: ✅ Compatible

Follow-up TODOs: None
================================================================================
-->

# Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development Mandate

All development work in the Evolution of Todo project MUST follow the Spec-Driven Development (SDD) methodology. This is the supreme workflow governing all agents and contributors.

**Non-Negotiable Rules:**
- No agent or contributor MAY write production code without approved specifications and tasks
- All work MUST follow the canonical workflow: **Constitution → Specs → Plan → Tasks → Implement**
- Specifications MUST be approved before planning begins
- Plans MUST be approved before task generation
- Tasks MUST be approved before implementation starts
- Every code change MUST trace back to an approved task

**Rationale:** SDD ensures traceability, prevents scope creep, and maintains architectural integrity across all five phases of the project. Without this discipline, the multi-phase evolution will become unmanageable.

### II. Agent Behavior Rules

All AI agents and human contributors MUST adhere to strict behavioral constraints to maintain project integrity.

**Non-Negotiable Rules:**
- **No manual coding by humans** - All code MUST be generated through the SDD workflow via approved agents
- **No feature invention** - Agents MUST NOT introduce features, patterns, or capabilities not explicitly defined in approved specifications
- **No deviation from specifications** - Implementation MUST match approved specs exactly; creative interpretation is forbidden
- **Refinement at spec level only** - When changes are needed, they MUST be made by updating specifications, not by modifying code directly
- **No premature optimization** - Agents MUST implement the simplest solution that satisfies the specification
- **No cross-phase leakage** - Agents MUST NOT implement features planned for future phases

**Rationale:** Strict agent governance ensures reproducibility, auditability, and prevents the accumulation of technical debt through ad-hoc decisions.

### III. Phase Governance

The Evolution of Todo project spans five distinct phases, each with strictly scoped boundaries.

**Phase Definitions:**
- **Phase I**: In-Memory Python Console App - Pure Python CLI todo application with in-memory storage
- **Phase II**: Full-Stack Web Application - Next.js frontend with FastAPI backend, SQLModel ORM, Neon DB persistence
- **Phase III**: AI-Powered Todo Chatbot - OpenAI ChatKit integration, Agents SDK, Official MCP SDK for AI assistance
- **Phase IV**: Local Kubernetes Deployment - Docker containerization, Minikube, Helm charts, kubectl-ai, kagent
- **Phase V**: Advanced Cloud Deployment - Kafka messaging, Dapr distributed runtime, DigitalOcean DOKS

**Non-Negotiable Rules:**
- Each phase MUST be strictly scoped by its specification document
- Future-phase features MUST NEVER leak into earlier phases
- Architecture MAY evolve only through updated and approved specs and plans
- Phase completion requires all acceptance criteria to be met
- No phase MAY begin implementation until its predecessor is complete or explicitly decoupled
- Cross-phase dependencies MUST be documented in specifications

**Rationale:** Phase governance prevents premature complexity and ensures each evolution stage is stable before adding new capabilities.

### IV. Technology Constraints

The following technology stack is mandated per phase. Deviations require explicit ADR documentation and approval.

**Phase I: In-Memory Console App**
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Development Tool**: Claude Code
- **Methodology**: Spec-Kit Plus (SDD framework)
- **Storage**: In-memory (no persistence)

**Phase II: Full-Stack Web Application**
- **Frontend**: Next.js 16+ (App Router), TypeScript
- **Backend**: FastAPI, Python 3.13+
- **ORM/Models**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens

**Phase III: AI-Powered Chatbot**
- **Chat Interface**: OpenAI ChatKit
- **Agent Framework**: OpenAI Agents SDK
- **Protocol**: Official MCP SDK (Model Context Protocol)

**Phase IV: Local Kubernetes Deployment**
- **Containerization**: Docker
- **Local Orchestration**: Minikube
- **Package Management**: Helm
- **AI-Assisted Kubectl**: kubectl-ai
- **Kubernetes Agent**: kagent

**Phase V: Advanced Cloud Deployment**
- **Messaging**: Apache Kafka (Redpanda/Strimzi/Confluent)
- **Distributed Runtime**: Dapr (Pub/Sub, State, Bindings, Secrets)
- **Cloud Platform**: Azure AKS, Google GKE, or Oracle OKE

**Non-Negotiable Rules:**
- All technology choices MUST align with the phase-specific stack above
- Alternative libraries MUST be justified via ADR before adoption
- Version pinning is REQUIRED for all dependencies
- No experimental or alpha-stage dependencies in production code
- Phase I MUST NOT include any database or web framework code

**Rationale:** A phase-constrained technology stack ensures each evolution stage introduces complexity incrementally and prevents premature architecture decisions.

### VI. Feature Tiers

Features MUST be implemented according to these tiers, respecting phase boundaries.

**Basic Level (Phase I-II Core):**
- Add Task – Create new todo items
- Delete Task – Remove tasks from the list
- Update Task – Modify existing task details
- View Task List – Display all tasks
- Mark as Complete – Toggle task completion status

**Intermediate Level (Phase II+):**
- Priorities & Tags – Assign levels (high/medium/low) or labels
- Search & Filter – Search by keyword; filter by status, priority, or date
- Sort Tasks – Reorder by due date, priority, or alphabetically

**Advanced Level (Phase V):**
- Recurring Tasks – Auto-reschedule repeating tasks
- Due Dates & Reminders – Set deadlines with notifications

**Non-Negotiable Rules:**
- Basic Level features MUST be complete before Intermediate
- Advanced features MUST NOT be implemented before Phase V
- Feature scope MUST match the approved specification

### VII. Monorepo Structure

All full-stack phases (II+) MUST follow this monorepo organization.

```
project-root/
├── .specify/              # Spec-Kit configuration
├── specs/                 # Feature specifications
│   ├── features/          # Feature specs
│   ├── api/               # API specifications
│   └── database/          # Schema specs
├── frontend/              # Next.js application
│   └── CLAUDE.md          # Frontend-specific guidelines
├── backend/               # FastAPI application
│   └── CLAUDE.md          # Backend-specific guidelines
├── CLAUDE.md              # Root Claude Code instructions
└── README.md
```

**Non-Negotiable Rules:**
- Specs folder MUST contain all specification artifacts
- Each service (frontend/backend) MUST have its own CLAUDE.md
- Root CLAUDE.md MUST reference AGENTS.md patterns

### VIII. Quality Principles

All code and artifacts MUST meet these quality standards regardless of phase.

**Clean Architecture:**
- Clear separation of concerns: models, services, API layers, and CLI MUST be distinct
- Dependencies MUST flow inward (infrastructure → application → domain)
- Business logic MUST NOT depend on framework-specific code

**Stateless Services:**
- API services MUST be stateless where required for scalability
- Session state MUST be externalized to database or cache
- No in-memory state that cannot survive process restart

**Cloud-Native Readiness:**
- All services MUST be containerizable from Phase I
- Configuration MUST be externalized via environment variables
- Health check endpoints MUST be implemented
- Graceful shutdown MUST be supported

**Testing Standards:**
- Unit tests for business logic
- Integration tests for API contracts
- Contract tests for external dependencies
- Test coverage reports MUST be generated

**Non-Negotiable Rules:**
- Code that violates separation of concerns MUST be refactored before merge
- Hardcoded configuration values are FORBIDDEN
- All public APIs MUST have documented contracts

**Rationale:** Quality principles ensure the codebase remains maintainable and scalable as it evolves through all five phases.

## Phase Overview

This section provides a high-level roadmap of all project phases.

| Phase | Name | Technology Stack | Dependencies |
|-------|------|------------------|--------------|
| I | In-Memory Python Console App | Python, Claude Code, Spec-Kit Plus | None |
| II | Full-Stack Web Application | Next.js, FastAPI, SQLModel, Neon DB | Phase I (concept) |
| III | AI-Powered Todo Chatbot | OpenAI ChatKit, Agents SDK, Official MCP SDK | Phase II |
| IV | Local Kubernetes Deployment | Docker, Minikube, Helm, kubectl-ai, kagent | Phase II, III |
| V | Advanced Cloud Deployment | Kafka, Dapr, DigitalOcean DOKS | Phase IV |

**Phase Transition Criteria:**
- All acceptance tests pass
- Documentation complete
- No critical bugs open
- Architecture review approved

## Development Workflow

All development MUST follow this workflow without exception.

**Step 1: Specification (`/sp.specify`)**
- Define feature requirements
- Document user stories with acceptance criteria
- Identify edge cases and constraints

**Step 2: Planning (`/sp.plan`)**
- Create architectural plan
- Define technical approach
- Document data models and API contracts
- Constitution Check MUST pass

**Step 3: Task Generation (`/sp.tasks`)**
- Break plan into atomic, testable tasks
- Assign dependencies and parallelization markers
- Map tasks to user stories

**Step 4: Implementation (`/sp.implement`)**
- Execute tasks in dependency order
- Follow test-first approach when specified
- Create PHR for each significant interaction

**Step 5: Review and Merge**
- Code review against specification
- All tests pass
- Documentation updated

**Forbidden Shortcuts:**
- Direct code commits without approved tasks
- Specification changes during implementation (must restart workflow)
- Skipping Constitution Check in planning

## Governance

This constitution is the supreme governing document for the Evolution of Todo project. All agents, contributors, and artifacts MUST comply.

**Amendment Process:**
1. Propose amendment via spec document
2. Document rationale and impact analysis
3. Obtain explicit approval from project owner
4. Update constitution with new version
5. Propagate changes to dependent templates

**Versioning Policy:**
- MAJOR: Backward-incompatible principle changes or removals
- MINOR: New principles, sections, or material expansions
- PATCH: Clarifications, typos, non-semantic refinements

**Compliance Requirements:**
- All PRs MUST reference compliance with relevant principles
- Violations MUST be documented and remediated before merge
- Periodic compliance audits MAY be conducted

**Architectural Decision Records:**
- Significant decisions MUST be documented via ADR
- ADRs MUST reference relevant constitutional principles
- ADR suggestions MUST be surfaced during planning phase

**Version**: 1.2.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
