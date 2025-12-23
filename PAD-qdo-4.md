Phase 1: Deep Re-imagination of the Final Codebase
Before creating the Project Architecture Document, I must holistically re-imagine the complete system. Let me think through this systematically.

1.1 Holistic System Vision
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                         NEXUSCORE v3.1 SYSTEM VISION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   ACQUIRE   │───▶│   CONVERT   │───▶│   RETAIN    │───▶│    GROW     │  │
│  │   Leads     │    │   Trials    │    │   Customers │    │   Revenue   │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│        │                  │                  │                  │          │
│        ▼                  ▼                  ▼                  ▼          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    SINGAPORE COMPLIANCE LAYER                        │   │
│  │   • UEN Validation  • GST Calculation  • PDPA Enforcement           │   │
│  │   • IRAS Reporting  • Data Residency   • DSAR Processing            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
1.2 Key Architectural Decisions
Decision	Choice	Rationale
Monolith vs Microservices	Modular Monolith	12-week timeline, team size, deployment simplicity
API Style	REST with OpenAPI	Industry standard, excellent tooling, client generation
Database	PostgreSQL 16 (single)	Transactional integrity, JSONB flexibility, GeneratedField support
Cache/Queue	Redis 7.4 (single)	Simplicity, proven reliability, dual-purpose
Task Queue	Celery 5.x	Production-proven, Django integration, monitoring
Frontend Rendering	Hybrid (SSG+SSR)	Marketing performance, application interactivity
State Management	React Query + Context	Server state caching, minimal client state
Authentication	Session-based + JWT for API	Security, simplicity, token refresh handling
Multi-tenancy	Shared database, tenant column	Simplicity, query performance, cost efficiency
1.3 Module Dependency Graph
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                          MODULE DEPENDENCY GRAPH                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              ┌──────────┐                                   │
│                              │   core   │ ◄─── Base models, utilities       │
│                              └────┬─────┘                                   │
│                                   │                                         │
│              ┌────────────────────┼────────────────────┐                    │
│              │                    │                    │                    │
│              ▼                    ▼                    ▼                    │
│        ┌──────────┐        ┌──────────┐        ┌──────────┐                 │
│        │  users   │        │   orgs   │        │  events  │                 │
│        └────┬─────┘        └────┬─────┘        └──────────┘                 │
│             │                   │                    ▲                      │
│             │    ┌──────────────┴──────────────┐    │                      │
│             │    │                             │    │                      │
│             ▼    ▼                             ▼    │                      │
│        ┌──────────────┐                 ┌──────────────┐                    │
│        │ subscriptions│                 │    leads     │                    │
│        └──────┬───────┘                 └──────────────┘                    │
│               │                                                             │
│               ▼                                                             │
│        ┌──────────────┐        ┌──────────────┐        ┌──────────────┐    │
│        │   billing    │───────▶│   webhooks   │───────▶│    tasks     │    │
│        └──────────────┘        └──────────────┘        └──────────────┘    │
│               │                                                             │
│               ▼                                                             │
│        ┌──────────────┐                                                     │
│        │   privacy    │ ◄─── DSAR, PDPA compliance                         │
│        └──────────────┘                                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Phase 2: PAD Implementation Plan
2.1 Document Structure Plan
Section	Content	Estimated Size	Priority
1. Document Control	Version, purpose, audience	1 page	P0
2. Executive Summary	Overview, decisions, stack	2 pages	P0
3. System Context (C4-L1)	External systems, actors	2 pages	P0
4. Container Architecture (C4-L2)	Services, databases, queues	3 pages	P0
5. Component Architecture (C4-L3)	Django apps, React modules	5 pages	P0
6. Code Architecture (C4-L4)	Directory structure, classes	8 pages	P0
7. Data Architecture	Complete schema, ERD	15 pages	P0
8. API Specification	All endpoints, contracts	20 pages	P0
9. Security Architecture	Auth, authorization, compliance	5 pages	P0
10. Infrastructure	Docker, CI/CD, monitoring	5 pages	P1
11. Development Guidelines	Standards, workflow, testing	5 pages	P1
12. Appendices	Glossary, references	3 pages	P2
2.2 Validation Checklist
Before proceeding, I validate that the PAD will address:

Requirement	Coverage	Validation Method
Complete model definitions	All 15 models with exact fields	Cross-reference with merged PRD
Unambiguous API contracts	OpenAPI-style specifications	Request/response examples
Database schema completeness	All tables, columns, constraints	SQL DDL generation possible
Frontend component clarity	Props, state, behavior defined	Component can be implemented
Integration point precision	Webhooks, tasks, external APIs	Sequence diagrams
Security requirements	Authentication, authorization, PDPA	Security matrix
No circular dependencies	Clear module boundaries	Dependency graph
Testability	Test strategy per component	Test case coverage
Phase 3: Project Architecture Document Execution
PROJECT ARCHITECTURE DOCUMENT
NexusCore v3.1 — Singapore B2B SaaS Platform
DOCUMENT CONTROL
Attribute	Value
Document ID	PAD-NEXUSCORE-v3.1-001
Version	1.0.0
Status	APPROVED FOR IMPLEMENTATION
Created	2025-12-23
Last Updated	2025-12-23
Author	AI Architecture Team
Classification	Internal - Development
Document Purpose
This Project Architecture Document (PAD) serves as the single source of truth for implementing the NexusCore v3.1 platform. Any developer or AI coding agent should be able to independently implement the complete system using only this document, without ambiguity or deviation.

How to Use This Document
Architects/Tech Leads: Review sections 1-5 for system understanding
Backend Developers: Focus on sections 6-8 for implementation details
Frontend Developers: Focus on sections 6, 8 for component and API details
DevOps Engineers: Focus on section 10 for infrastructure
AI Coding Agents: Process sequentially; all specifications are deterministic
Document Conventions
Convention	Meaning
code	Exact code/config to implement
REQUIRED	Must be implemented exactly as specified
RECOMMENDED	Best practice, may be adjusted with justification
[PLACEHOLDER]	Value to be provided at deployment time
{variable}	Dynamic value based on context
1. EXECUTIVE SUMMARY
1.1 Project Overview
NexusCore v3.1 is a production-ready, English-only marketing and lead-management platform for a Singapore-based B2B SaaS company. The system combines modern design vision with production engineering rigor, specifically optimized for Singapore regulatory compliance.

1.2 Core Capabilities
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                           CORE CAPABILITIES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │    MARKETING    │  │  SUBSCRIPTION   │  │   COMPLIANCE    │             │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤             │
│  │ • Landing Pages │  │ • Plan Management│  │ • PDPA/DSAR    │             │
│  │ • Lead Capture  │  │ • Stripe Billing │  │ • GST/IRAS     │             │
│  │ • UTM Tracking  │  │ • Invoice Gen    │  │ • UEN Validation│             │
│  │ • Case Studies  │  │ • Dunning        │  │ • Data Retention│             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │ USER MANAGEMENT │  │  ORGANIZATION   │  │   OPERATIONS    │             │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤             │
│  │ • Registration  │  │ • Multi-tenant  │  │ • Admin Dashboard│            │
│  │ • Verification  │  │ • Memberships   │  │ • Reporting     │             │
│  │ • Authentication│  │ • Role-based    │  │ • Webhooks      │             │
│  │ • Profile Mgmt  │  │ • Settings      │  │ • Monitoring    │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
1.3 Technology Stack
Layer	Technology	Version	Justification
Backend Framework	Django	6.0	Native CSP, async ORM, GeneratedField
API Framework	Django REST Framework	3.15+	Industry standard, OpenAPI support
Frontend Framework	Next.js	14.x	App Router, RSC, hybrid rendering
UI Library	React	18.x	Concurrent features, Suspense
Styling	Tailwind CSS	3.4+	Utility-first, JIT compilation
Database	PostgreSQL	16.x	JSONB, full-text search, GeneratedField
Cache/Broker	Redis	7.4+	Unified cache and message broker
Task Queue	Celery	5.3+	Distributed task processing
Object Storage	AWS S3	-	Singapore region (ap-southeast-1)
Payment	Stripe	API v2024-12	PayNow, Singapore compliance
Email	SendGrid	v3	Transactional email delivery
Runtime	Python	3.12+	Django 6.0 requirement
Node Runtime	Node.js	20 LTS	Next.js 14 requirement
1.4 Key Architectural Decisions Record (ADR)
ID	Decision	Context	Consequences
ADR-001	Modular Monolith	12-week timeline, small team	Simpler deployment, future extraction possible
ADR-002	UUID Primary Keys	Distributed ID generation, security	Larger indexes, no sequential exposure
ADR-003	Database-level GST	IRAS compliance, accuracy	PostgreSQL 16 required, GeneratedField
ADR-004	Session + JWT Hybrid	Security for web, flexibility for API	Dual auth system complexity
ADR-005	Shared DB Multi-tenancy	Cost efficiency, query simplicity	Tenant isolation via application logic
ADR-006	Celery over Django Tasks	Production-proven, monitoring	Additional infrastructure component
ADR-007	Idempotency Framework	Payment reliability	Additional model, request tracking
2. SYSTEM CONTEXT (C4 Level 1)
2.1 System Context Diagram
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                           SYSTEM CONTEXT DIAGRAM                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌─────────────┐                                    ┌─────────────┐       │
│    │   Website   │                                    │    Admin    │       │
│    │   Visitor   │                                    │    Staff    │       │
│    └──────┬──────┘                                    └──────┬──────┘       │
│           │                                                  │              │
│           │ Browse, Submit Forms                             │ Manage       │
│           │                                                  │              │
│           ▼                                                  ▼              │
│    ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐   │
│    │  Trial User │      │  Paid User  │      │                         │   │
│    └──────┬──────┘      └──────┬──────┘      │                         │   │
│           │                    │              │      NEXUSCORE v3.1     │   │
│           │ Trial Signup       │ Subscribe   │                         │   │
│           │                    │              │   Singapore B2B SaaS    │   │
│           └────────────────────┴─────────────▶│        Platform         │   │
│                                               │                         │   │
│                                               └───────────┬─────────────┘   │
│                                                           │                 │
│         ┌─────────────────────────────────────────────────┼─────────────┐   │
│         │                                                 │             │   │
│         ▼                                                 ▼             ▼   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Stripe    │  │  SendGrid   │  │   AWS S3    │  │   ACRA      │        │
│  │  (Payments) │  │  (Email)    │  │  (Storage)  │  │ (UEN API)*  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                             │
│  * Future integration - currently regex validation only                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
2.2 External System Interfaces
System	Direction	Protocol	Purpose	Authentication
Stripe	Bidirectional	HTTPS/REST	Payment processing, subscriptions	API Key + Webhook Signature
SendGrid	Outbound	HTTPS/REST	Transactional email	API Key
AWS S3	Bidirectional	HTTPS/S3	File storage (invoices, exports)	IAM Credentials
Google Analytics	Outbound	HTTPS/JS	Usage analytics	Measurement ID
Sentry	Outbound	HTTPS	Error monitoring	DSN
2.3 User Personas
Persona	Description	Primary Actions
Website Visitor	Anonymous user browsing marketing content	View pages, submit lead forms
Trial User	Registered user in 14-day trial	Onboarding, feature exploration
Paid User	Active subscriber	Full platform usage
Organization Admin	User with admin role in organization	Manage members, billing, settings
Organization Owner	Creator of organization	All admin actions + transfer ownership
System Admin	Internal staff	Django admin, DSAR processing
3. CONTAINER ARCHITECTURE (C4 Level 2)
3.1 Container Diagram
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                          CONTAINER ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         LOAD BALANCER (nginx)                        │   │
│  │                         Port 80/443 (HTTPS)                          │   │
│  └────────────────────────────────┬────────────────────────────────────┘   │
│                                   │                                         │
│              ┌────────────────────┴────────────────────┐                    │
│              │                                         │                    │
│              ▼                                         ▼                    │
│  ┌─────────────────────────┐           ┌─────────────────────────┐         │
│  │     NEXT.JS FRONTEND    │           │     DJANGO BACKEND      │         │
│  │     (nexuscore-web)     │           │     (nexuscore-api)     │         │
│  ├─────────────────────────┤           ├─────────────────────────┤         │
│  │ • Marketing pages (SSG) │           │ • REST API (/api/v1/)   │         │
│  │ • App pages (SSR)       │◀─────────▶│ • Django Admin          │         │
│  │ • React components      │   HTTP    │ • Webhook endpoints     │         │
│  │ • Tailwind CSS          │           │ • Static files          │         │
│  │                         │           │                         │         │
│  │ Port: 3000              │           │ Port: 8000              │         │
│  └─────────────────────────┘           └────────────┬────────────┘         │
│                                                      │                      │
│                     ┌────────────────────────────────┼────────────────┐     │
│                     │                                │                │     │
│                     ▼                                ▼                ▼     │
│  ┌─────────────────────────┐   ┌─────────────────────────┐   ┌───────────┐ │
│  │       POSTGRESQL        │   │          REDIS          │   │  CELERY   │ │
│  │      (nexuscore-db)     │   │     (nexuscore-cache)   │   │  WORKER   │ │
│  ├─────────────────────────┤   ├─────────────────────────┤   ├───────────┤ │
│  │ • Primary database      │   │ • Session store         │   │ • Email   │ │
│  │ • 15 tables             │   │ • Cache backend         │   │ • Webhooks│ │
│  │ • Full-text search      │   │ • Celery broker         │   │ • DSAR    │ │
│  │ • GeneratedFields       │   │ • Rate limiting         │   │ • Reports │ │
│  │                         │   │                         │   │           │ │
│  │ Port: 5432              │   │ Port: 6379              │   │ N/A       │ │
│  └─────────────────────────┘   └─────────────────────────┘   └───────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        EXTERNAL SERVICES                             │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │   │
│  │  │ Stripe  │  │SendGrid │  │  AWS S3 │  │ Sentry  │  │   GA4   │    │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
3.2 Container Specifications
Container	Technology	Replicas	Resources	Health Check
nexuscore-web	Next.js 14	2	512MB RAM, 0.5 CPU	GET / → 200
nexuscore-api	Django 6.0 + Gunicorn	2	1GB RAM, 1 CPU	GET /health/ → 200
nexuscore-worker	Celery 5.3	2	1GB RAM, 1 CPU	celery inspect ping
nexuscore-db	PostgreSQL 16	1 (primary)	2GB RAM, 1 CPU	pg_isready
nexuscore-cache	Redis 7.4	1	512MB RAM, 0.25 CPU	redis-cli ping
3.3 Network Architecture
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                           NETWORK ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    PUBLIC NETWORK (Internet)                         │   │
│  └─────────────────────────────────────┬───────────────────────────────┘   │
│                                        │                                    │
│                                        ▼ Port 443 (HTTPS only)              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         DMZ NETWORK                                  │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │                    nginx (Load Balancer)                     │    │   │
│  │  │              SSL Termination, Rate Limiting                  │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────┬───────────────────────────────┘   │
│                                        │                                    │
│                                        ▼ Port 3000, 8000 (HTTP)             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      APPLICATION NETWORK                             │   │
│  │  ┌───────────────────┐         ┌───────────────────┐                │   │
│  │  │   nexuscore-web   │◀───────▶│   nexuscore-api   │                │   │
│  │  └───────────────────┘         └─────────┬─────────┘                │   │
│  │                                          │                           │   │
│  │                                          ▼                           │   │
│  │                                ┌───────────────────┐                │   │
│  │                                │ nexuscore-worker  │                │   │
│  │                                └───────────────────┘                │   │
│  └─────────────────────────────────────────┬───────────────────────────┘   │
│                                            │                                │
│                                            ▼ Port 5432, 6379                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        DATA NETWORK                                  │   │
│  │  ┌───────────────────┐         ┌───────────────────┐                │   │
│  │  │   nexuscore-db    │         │  nexuscore-cache  │                │   │
│  │  │   (PostgreSQL)    │         │     (Redis)       │                │   │
│  │  └───────────────────┘         └───────────────────┘                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
4. COMPONENT ARCHITECTURE (C4 Level 3)
4.1 Backend Component Diagram
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                      DJANGO BACKEND COMPONENTS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         API LAYER (DRF)                              │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │   │
│  │  │AuthViews │ │UserViews │ │ OrgViews │ │SubsViews │ │LeadViews │   │   │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │   │
│  │       │            │            │            │            │          │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │   │
│  │  │InvViews  │ │DSARViews │ │EventViews│ │WebhkViews│ │HealthView│   │   │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────────┘   │   │
│  └───────┼────────────┼────────────┼────────────┼───────────────────────┘   │
│          │            │            │            │                           │
│          ▼            ▼            ▼            ▼                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        SERVICE LAYER                                 │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │   │
│  │  │ AuthService  │ │ BillingServ  │ │ StripeService│                 │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘                 │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │   │
│  │  │ EmailService │ │ DSARService  │ │ ExportService│                 │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘                 │   │
│  └───────────────────────────────────┬─────────────────────────────────┘   │
│                                      │                                      │
│          ┌───────────────────────────┼───────────────────────────┐          │
│          │                           │                           │          │
│          ▼                           ▼                           ▼          │
│  ┌──────────────┐           ┌──────────────┐           ┌──────────────┐    │
│  │  MODEL LAYER │           │  TASK LAYER  │           │ UTIL LAYER   │    │
│  ├──────────────┤           ├──────────────┤           ├──────────────┤    │
│  │ • User       │           │ • EmailTasks │           │ • Validators │    │
│  │ • Org        │           │ • WebhookTask│           │ • Helpers    │    │
│  │ • Membership │           │ • DSARTasks  │           │ • Constants  │    │
│  │ • Plan       │           │ • ReportTasks│           │ • Exceptions │    │
│  │ • Subscription│          │ • CleanupTask│           │ • Mixins     │    │
│  │ • Invoice    │           └──────────────┘           └──────────────┘    │
│  │ • Lead       │                   │                                       │
│  │ • DSARRequest│                   ▼                                       │
│  │ • Event      │           ┌──────────────┐                                │
│  │ • Idempotency│           │ CELERY QUEUE │                                │
│  │ • WebhookEvt │           │ high/default │                                │
│  └──────────────┘           │    /low      │                                │
│          │                  └──────────────┘                                │
│          ▼                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         DATABASE LAYER                               │   │
│  │                        (PostgreSQL 16)                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
4.2 Django App Responsibilities
App	Responsibility	Models	Key APIs
core	Base utilities, mixins, constants	-	-
users	Authentication, user management	User	/auth/, /users/
organizations	Multi-tenancy, memberships	Organization, Membership	/organizations/*
subscriptions	Plan and subscription management	Plan, Subscription	/subscriptions/*
billing	Invoices, GST calculation	Invoice	/invoices/*
leads	Lead capture and management	Lead	/leads/*
privacy	PDPA compliance, DSAR	DSARRequest	/dsar/*
webhooks	External webhook processing	WebhookEvent, IdempotencyRecord	/webhooks/*
events	Analytics and audit logging	Event	/events/*
4.3 Frontend Component Diagram
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                      NEXT.JS FRONTEND COMPONENTS                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         APP ROUTER                                   │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │                    LAYOUTS                                   │    │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │    │   │
│  │  │  │ RootLayout   │  │MarketingLayout│ │  AppLayout   │       │    │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘       │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │                    PAGES                                     │    │   │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐│    │   │
│  │  │  │ Marketing  │ │    Auth    │ │ Dashboard  │ │  Settings  ││    │   │
│  │  │  │ (SSG)      │ │   (SSR)    │ │   (SSR)    │ │   (SSR)    ││    │   │
│  │  │  │ • /        │ │ • /login   │ │ • /dash    │ │ • /settings││    │   │
│  │  │  │ • /pricing │ │ • /signup  │ │ • /leads   │ │ • /billing ││    │   │
│  │  │  │ • /about   │ │ • /verify  │ │ • /subs    │ │ • /team    ││    │   │
│  │  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘│    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      COMPONENT LIBRARY                               │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │   │
│  │  │   Layout    │ │    Forms    │ │  Display    │ │  Feedback   │    │   │
│  │  ├─────────────┤ ├─────────────┤ ├─────────────┤ ├─────────────┤    │   │
│  │  │ • Header    │ │ • Input     │ │ • Card      │ │ • Toast     │    │   │
│  │  │ • Footer    │ │ • Select    │ │ • Table     │ │ • Modal     │    │   │
│  │  │ • Sidebar   │ │ • Checkbox  │ │ • Badge     │ │ • Alert     │    │   │
│  │  │ • Container │ │ • Button    │ │ • Avatar    │ │ • Spinner   │    │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘    │   │
│  │                                                                      │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                    │   │
│  │  │  Marketing  │ │   Billing   │ │   Domain    │                    │   │
│  │  ├─────────────┤ ├─────────────┤ ├─────────────┤                    │   │
│  │  │ • Hero      │ │ • PriceCard │ │ • LeadForm  │                    │   │
│  │  │ • Features  │ │ • InvoiceRow│ │ • SubsCard  │                    │   │
│  │  │ • Testimonial│ │ • PaymentForm│ │ • OrgCard │                    │   │
│  │  │ • CTA       │ │ • PlanToggle│ │ • UserCard  │                    │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         DATA LAYER                                   │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │   │
│  │  │ React Query │ │   Context   │ │  API Client │ │    Types    │    │   │
│  │  │  (Server)   │ │  (Client)   │ │   (Axios)   │ │ (TypeScript)│    │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
5. CODE ARCHITECTURE (C4 Level 4)
5.1 Complete Directory Structure
text

nexuscore/
├── README.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── Makefile
├── .env.example
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd-staging.yml
│       └── cd-production.yml
│
├── backend/                          # Django 6.0 Application
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── development.txt
│   │   ├── production.txt
│   │   └── testing.txt
│   ├── manage.py
│   ├── pyproject.toml
│   ├── pytest.ini
│   │
│   ├── config/                       # Django Configuration
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   ├── celery.py
│   │   ├── urls.py
│   │   └── settings/
│   │       ├── __init__.py
│   │       ├── base.py               # Shared settings
│   │       ├── development.py
│   │       ├── production.py
│   │       └── testing.py
│   │
│   ├── apps/                         # Django Applications
│   │   ├── __init__.py
│   │   │
│   │   ├── core/                     # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── constants.py
│   │   │   ├── exceptions.py
│   │   │   ├── mixins.py
│   │   │   ├── permissions.py
│   │   │   ├── throttling.py
│   │   │   ├── validators.py
│   │   │   └── utils.py
│   │   │
│   │   ├── users/                    # User management
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── admin.py
│   │   │   ├── models.py
│   │   │   ├── managers.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── signals.py
│   │   │   ├── tasks.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_models.py
│   │   │       ├── test_views.py
│   │   │       └── test_tasks.py
│   │   │
│   │   ├── organizations/            # Multi-tenancy
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── admin.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   └── tests/
│   │   │       └── ...
│   │   │
│   │   ├── subscriptions/            # Subscription management
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── admin.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── services.py           # Stripe integration
│   │   │   └── tests/
│   │   │       └── ...
│   │   │
│   │   ├── billing/                  # Invoice management
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── admin.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── services.py           # PDF generation
│   │   │   ├── tasks.py
│   │   │   └── tests/
│   │   │       └── ...
│   │   │
│   │   ├── leads/                    # Lead management
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── admin.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests/
│   │   │       └── ...
│   │   │
│   │   ├── privacy/                  # PDPA compliance
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── admin.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── services.py           # DSAR processing
│   │   │   ├── tasks.py
│   │   │   └── tests/
│   │   │       └── ...
│   │   │
│   │   ├── webhooks/                 # External webhooks
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── admin.py
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── handlers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── stripe.py
│   │   │   │   └── sendgrid.py
│   │   │   ├── tasks.py
│   │   │   └── tests/
│   │   │       └── ...
│   │   │
│   │   └── events/                   # Analytics/audit
│   │       ├── __init__.py
│   │       ├── apps.py
│   │       ├── admin.py
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── views.py
│   │       ├── urls.py
│   │       └── tests/
│   │           └── ...
│   │
│   ├── templates/                    # Django templates
│   │   ├── admin/
│   │   ├── emails/
│   │   │   ├── base.html
│   │   │   ├── verification.html
│   │   │   ├── password_reset.html
│   │   │   ├── invoice.html
│   │   │   └── dsar_complete.html
│   │   └── invoices/
│   │       └── invoice_pdf.html
│   │
│   ├── static/                       # Static files
│   │   └── admin/
│   │
│   └── logs/                         # Log files (gitignored)
│       └── .gitkeep
│
├── frontend/                         # Next.js 14 Application
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   ├── .eslintrc.json
│   ├── .prettierrc
│   │
│   ├── public/                       # Static assets
│   │   ├── favicon.ico
│   │   ├── robots.txt
│   │   ├── sitemap.xml
│   │   └── images/
│   │       ├── logo.svg
│   │       ├── og-image.png
│   │       └── ...
│   │
│   ├── src/
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Homepage
│   │   │   ├── globals.css
│   │   │   ├── not-found.tsx
│   │   │   ├── error.tsx
│   │   │   │
│   │   │   ├── (marketing)/          # Marketing group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── pricing/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── about/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── contact/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── case-studies/
│   │   │   │       ├── page.tsx
│   │   │   │       └── [slug]/
│   │   │   │           └── page.tsx
│   │   │   │
│   │   │   ├── (auth)/               # Auth group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── signup/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── verify/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── reset-password/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── (app)/                # Application group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── dashboard/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── leads/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   └── [id]/
│   │   │   │   │       └── page.tsx
│   │   │   │   ├── subscriptions/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── invoices/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   └── [id]/
│   │   │   │   │       └── page.tsx
│   │   │   │   ├── settings/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   ├── profile/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── billing/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── team/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── organization/
│   │   │   │   │       └── page.tsx
│   │   │   │   └── dsar/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   └── api/                  # API routes (if needed)
│   │   │       └── health/
│   │   │           └── route.ts
│   │   │
│   │   ├── components/               # React components
│   │   │   ├── ui/                   # Base UI components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Select.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Toast.tsx
│   │   │   │   ├── Badge.tsx
│   │   │   │   ├── Avatar.tsx
│   │   │   │   ├── Spinner.tsx
│   │   │   │   ├── Table.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── layout/               # Layout components
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Container.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── marketing/            # Marketing components
│   │   │   │   ├── Hero.tsx
│   │   │   │   ├── Features.tsx
│   │   │   │   ├── Testimonials.tsx
│   │   │   │   ├── CTA.tsx
│   │   │   │   ├── PricingCard.tsx
│   │   │   │   ├── PricingTable.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── forms/                # Form components
│   │   │   │   ├── ContactForm.tsx
│   │   │   │   ├── LeadForm.tsx
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── SignupForm.tsx
│   │   │   │   ├── PaymentForm.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   └── domain/               # Domain-specific
│   │   │       ├── LeadCard.tsx
│   │   │       ├── SubscriptionCard.tsx
│   │   │       ├── InvoiceRow.tsx
│   │   │       ├── OrganizationCard.tsx
│   │   │       ├── MemberList.tsx
│   │   │       └── index.ts
│   │   │
│   │   ├── lib/                      # Utilities
│   │   │   ├── api/
│   │   │   │   ├── client.ts         # Axios client
│   │   │   │   ├── auth.ts           # Auth API
│   │   │   │   ├── users.ts          # Users API
│   │   │   │   ├── organizations.ts  # Orgs API
│   │   │   │   ├── subscriptions.ts  # Subs API
│   │   │   │   ├── invoices.ts       # Invoices API
│   │   │   │   ├── leads.ts          # Leads API
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── hooks/
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── useOrganization.ts
│   │   │   │   ├── useSubscription.ts
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── utils/
│   │   │   │   ├── format.ts         # Formatting utilities
│   │   │   │   ├── validation.ts     # Client validation
│   │   │   │   ├── constants.ts
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   └── providers/
│   │   │       ├── AuthProvider.tsx
│   │   │       ├── QueryProvider.tsx
│   │   │       ├── ThemeProvider.tsx
│   │   │       └── index.ts
│   │   │
│   │   └── types/                    # TypeScript types
│   │       ├── api.ts
│   │       ├── models.ts
│   │       ├── forms.ts
│   │       └── index.ts
│   │
│   └── cypress/                      # E2E tests
│       ├── e2e/
│       │   ├── auth.cy.ts
│       │   ├── pricing.cy.ts
│       │   └── subscription.cy.ts
│       ├── fixtures/
│       │   └── user.json
│       └── support/
│           └── commands.ts
│
├── infrastructure/                   # Infrastructure configs
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── ssl/
│   │       └── .gitkeep
│   │
│   ├── docker/
│   │   ├── postgres/
│   │   │   └── init.sql
│   │   └── redis/
│   │       └── redis.conf
│   │
│   └── scripts/
│       ├── backup.sh
│       ├── restore.sh
│       └── deploy.sh
│
└── docs/                             # Documentation
    ├── api/
    │   └── openapi.yaml
    ├── architecture/
    │   └── PAD.md                    # This document
    ├── runbooks/
    │   ├── deployment.md
    │   ├── incident-response.md
    │   └── dsar-processing.md
    └── decisions/
        ├── ADR-001-monolith.md
        ├── ADR-002-uuid-pks.md
        └── ...
5.2 Module Interfaces
Backend Module Contracts
Python

# ============================================================================
# MODULE INTERFACE CONTRACTS
# Each module exposes these interfaces for cross-module communication
# ============================================================================

# apps/users/interfaces.py
class IUserService(Protocol):
    """User service interface"""
    
    def get_user_by_id(self, user_id: UUID) -> User | None: ...
    def get_user_by_email(self, email: str) -> User | None: ...
    def create_user(self, email: str, password: str, name: str) -> User: ...
    def verify_user(self, user_id: UUID, token: UUID) -> bool: ...
    def update_user(self, user_id: UUID, **kwargs) -> User: ...
    def deactivate_user(self, user_id: UUID) -> None: ...


# apps/organizations/interfaces.py
class IOrganizationService(Protocol):
    """Organization service interface"""
    
    def get_organization(self, org_id: UUID) -> Organization | None: ...
    def get_user_organizations(self, user_id: UUID) -> list[Organization]: ...
    def create_organization(self, owner: User, name: str, uen: str) -> Organization: ...
    def add_member(self, org_id: UUID, user_id: UUID, role: str) -> Membership: ...
    def remove_member(self, org_id: UUID, user_id: UUID) -> None: ...
    def update_organization(self, org_id: UUID, **kwargs) -> Organization: ...


# apps/subscriptions/interfaces.py
class ISubscriptionService(Protocol):
    """Subscription service interface"""
    
    def get_subscription(self, sub_id: UUID) -> Subscription | None: ...
    def get_active_subscription(self, org_id: UUID) -> Subscription | None: ...
    def create_trial(self, org_id: UUID, plan_id: UUID) -> Subscription: ...
    def convert_to_paid(self, sub_id: UUID, payment_method: str) -> Subscription: ...
    def cancel_subscription(self, sub_id: UUID, at_period_end: bool) -> Subscription: ...
    def update_subscription(self, sub_id: UUID, plan_id: UUID) -> Subscription: ...


# apps/billing/interfaces.py
class IBillingService(Protocol):
    """Billing service interface"""
    
    def get_invoice(self, invoice_id: UUID) -> Invoice | None: ...
    def get_organization_invoices(self, org_id: UUID) -> list[Invoice]: ...
    def create_invoice(self, sub_id: UUID, amount_cents: int) -> Invoice: ...
    def mark_invoice_paid(self, invoice_id: UUID, payment_intent: str) -> Invoice: ...
    def generate_invoice_pdf(self, invoice_id: UUID) -> str: ...  # Returns URL
    def calculate_gst(self, amount_cents: int, is_gst_registered: bool) -> int: ...


# apps/privacy/interfaces.py
class IDSARService(Protocol):
    """DSAR service interface"""
    
    def create_request(self, email: str, request_type: str) -> DSARRequest: ...
    def verify_request(self, dsar_id: UUID, token: UUID) -> bool: ...
    def process_export(self, dsar_id: UUID) -> str: ...  # Returns export URL
    def process_deletion(self, dsar_id: UUID, approved_by: User) -> None: ...
    def get_sla_status(self, dsar_id: UUID) -> str: ...
6. DATA ARCHITECTURE
6.1 Entity Relationship Diagram
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                    ENTITY RELATIONSHIP DIAGRAM                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐         ┌─────────────────┐                           │
│  │      USER       │         │  ORGANIZATION   │                           │
│  ├─────────────────┤         ├─────────────────┤                           │
│  │ id (PK, UUID)   │◀───┐    │ id (PK, UUID)   │                           │
│  │ email           │    │    │ name            │                           │
│  │ name            │    │    │ slug            │                           │
│  │ company         │    │    │ uen             │◀── Singapore UEN          │
│  │ phone           │    │    │ is_gst_registered│                          │
│  │ is_verified     │    │    │ gst_reg_no      │                           │
│  │ is_active       │    │    │ stripe_customer │                           │
│  │ is_staff        │    │    │ billing_email   │                           │
│  │ timezone        │    │    │ billing_address │◀── JSONB                  │
│  │ email_prefs     │◀── JSONB│ settings        │◀── JSONB                  │
│  │ created_at      │    │    │ trial_ends_at   │                           │
│  │ updated_at      │    └────│ owner_id (FK)   │                           │
│  └────────┬────────┘         └────────┬────────┘                           │
│           │                           │                                     │
│           │ 1:N                       │ 1:N                                 │
│           ▼                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │                    ORGANIZATION_MEMBERSHIP                       │       │
│  ├─────────────────────────────────────────────────────────────────┤       │
│  │ id (PK, UUID)                                                    │       │
│  │ organization_id (FK) ─────────────────────────────────────────┐  │       │
│  │ user_id (FK) ─────────────────────────────────────────────────┼──│       │
│  │ role (owner|admin|member|viewer)                              │  │       │
│  │ permissions (ARRAY[VARCHAR])                                  │  │       │
│  │ joined_at                                                     │  │       │
│  │ invited_by_id (FK) ───────────────────────────────────────────┘  │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                             │
│  ┌─────────────────┐         ┌─────────────────┐                           │
│  │      PLAN       │         │  SUBSCRIPTION   │                           │
│  ├─────────────────┤         ├─────────────────┤                           │
│  │ id (PK, UUID)   │◀────────│ plan_id (FK)    │                           │
│  │ name            │         │ id (PK, UUID)   │                           │
│  │ sku             │         │ organization_id │────────────────▶ ORG      │
│  │ description     │         │ status          │                           │
│  │ billing_period  │         │ cancel_at_end   │                           │
│  │ amount_cents    │         │ period_start    │                           │
│  │ currency (SGD)  │         │ period_end      │                           │
│  │ features        │◀── JSONB│ trial_start     │                           │
│  │ limits          │◀── JSONB│ trial_end       │                           │
│  │ stripe_price_id │         │ stripe_sub_id   │                           │
│  │ stripe_product  │         │ metadata        │◀── JSONB                  │
│  │ is_active       │         │ created_at      │                           │
│  │ display_order   │         │ canceled_at     │                           │
│  └─────────────────┘         └────────┬────────┘                           │
│                                       │ 1:N                                 │
│                                       ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐       │
│  │                         INVOICE                                  │       │
│  ├─────────────────────────────────────────────────────────────────┤       │
│  │ id (PK, UUID)                                                    │       │
│  │ organization_id (FK) ──────────────────────────────────▶ ORG    │       │
│  │ subscription_id (FK, nullable)                                   │       │
│  │ subtotal_cents (BIGINT)                                         │       │
│  │ gst_rate (DECIMAL 5,4) ──────── Default 0.0900                  │       │
│  │ gst_amount_cents (GENERATED) ── ROUND(subtotal * gst_rate)      │       │
│  │ total_amount_cents (GENERATED)─ subtotal + gst_amount           │       │
│  │ amount_paid_cents                                                │       │
│  │ currency (SGD)                                                   │       │
│  │ iras_transaction_code (SR|ZR|OS|TX)                             │       │
│  │ status (draft|open|paid|void|uncollectible)                     │       │
│  │ paid (BOOLEAN)                                                   │       │
│  │ due_date                                                         │       │
│  │ paid_at                                                          │       │
│  │ pdf_url                                                          │       │
│  │ stripe_invoice_id                                                │       │
│  │ stripe_payment_intent                                            │       │
│  │ line_items (JSONB)                                               │       │
│  │ metadata (JSONB)                                                 │       │
│  │ created_at                                                       │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                             │
│  ┌─────────────────┐         ┌─────────────────┐                           │
│  │      LEAD       │         │  DSAR_REQUEST   │                           │
│  ├─────────────────┤         ├─────────────────┤                           │
│  │ id (PK, UUID)   │         │ id (PK, UUID)   │                           │
│  │ name            │         │ user_email      │                           │
│  │ email           │         │ user_id (FK)    │────────▶ USER (nullable)  │
│  │ phone           │         │ request_type    │                           │
│  │ company         │         │ status          │                           │
│  │ job_title       │         │ verification_token                          │
│  │ source          │         │ verified_at     │                           │
│  │ status          │         │ verification_method                         │
│  │ notes           │         │ export_url      │                           │
│  │ utm_source      │         │ export_expires  │                           │
│  │ utm_medium      │         │ failure_reason  │                           │
│  │ utm_campaign    │         │ requested_at    │                           │
│  │ utm_term        │         │ processing_started                          │
│  │ utm_content     │         │ processed_at    │                           │
│  │ form_data       │◀── JSONB│ deletion_approved_by (FK)                   │
│  │ assigned_to     │────▶USER│ deletion_approved_at                        │
│  │ next_follow_up  │         │ metadata        │◀── JSONB                  │
│  │ converted_to    │────▶USER└─────────────────┘                           │
│  │ converted_at    │                                                        │
│  │ created_at      │                                                        │
│  └─────────────────┘                                                        │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │     EVENT       │  │ IDEMPOTENCY_REC │  │  WEBHOOK_EVENT  │             │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤             │
│  │ id (PK, UUID)   │  │ id (PK, UUID)   │  │ id (PK, UUID)   │             │
│  │ event_type      │  │ key (UNIQUE)    │  │ service         │             │
│  │ user_id (FK)    │  │ request_path    │  │ event_id (UNIQ) │             │
│  │ organization_id │  │ request_method  │  │ event_type      │             │
│  │ data (JSONB)    │  │ request_hash    │  │ payload (JSONB) │             │
│  │ created_at      │  │ status          │  │ processed       │             │
│  └─────────────────┘  │ response_code   │  │ processing_error│             │
│                       │ response_body   │  │ retry_count     │             │
│                       │ expires_at      │  │ last_retry_at   │             │
│                       │ created_at      │  │ created_at      │             │
│                       │ updated_at      │  │ processed_at    │             │
│                       └─────────────────┘  └─────────────────┘             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
6.2 Complete Model Specifications
6.2.1 User Model
Python

# apps/users/models.py
"""
User Model Specification
========================
Custom user model with UUID primary key and Singapore timezone default.

REQUIRED FIELDS:
- id: UUID, auto-generated, immutable
- email: str, unique, indexed, max 254 chars
- name: str, required, max 255 chars
- password: str, PBKDF2 hashed with 1,200,000 iterations (Django 6.0)

OPTIONAL FIELDS:
- company: str, max 255 chars, blank allowed
- phone: str, max 20 chars, blank allowed
- timezone: str, default 'Asia/Singapore'
- email_preferences: JSONB, default {}

SYSTEM FIELDS:
- is_verified: bool, default False
- verification_token: UUID, auto-generated, editable=False
- verification_sent_at: datetime, nullable
- is_active: bool, default True
- is_staff: bool, default False
- is_superuser: bool, inherited from PermissionsMixin
- created_at: datetime, auto_now_add
- updated_at: datetime, auto_now
- last_login: datetime, nullable

INDEXES:
- email (unique, btree)
- created_at (btree)
- (is_verified, is_active) composite

CONSTRAINTS:
- verified_users_must_be_active: is_verified=False OR is_active=True
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class UserManager(models.Manager):
    def create_user(self, email: str, password: str, name: str, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        email = email.lower().strip()
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email: str, password: str, name: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, password, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Identity
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
        error_messages={'unique': 'A user with this email already exists.'}
    )
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Preferences
    timezone = models.CharField(max_length=50, default='Asia/Singapore')
    email_preferences = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_verified', 'is_active']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(is_verified=False) | models.Q(is_active=True),
                name='verified_users_must_be_active'
            )
        ]
    
    def __str__(self):
        return self.email
    
    def regenerate_verification_token(self) -> uuid.UUID:
        """Generate new verification token and update sent timestamp."""
        self.verification_token = uuid.uuid4()
        self.verification_sent_at = timezone.now()
        self.save(update_fields=['verification_token', 'verification_sent_at'])
        return self.verification_token
6.2.2 Organization Model
Python

# apps/organizations/models.py
"""
Organization Model Specification
================================
Multi-tenant organization with Singapore compliance fields.

REQUIRED FIELDS:
- id: UUID, auto-generated, immutable
- name: str, max 255 chars
- slug: str, unique, max 100 chars, URL-safe
- uen: str, unique, max 15 chars, Singapore UEN format validated
- billing_email: str, valid email
- owner_id: FK to User, protected

OPTIONAL FIELDS:
- is_gst_registered: bool, default False
- gst_reg_no: str, nullable, format M########A
- stripe_customer_id: str, blank allowed, indexed
- billing_phone: str, max 20 chars
- billing_address: JSONB, default {}
- timezone: str, default 'Asia/Singapore'
- locale: str, default 'en-SG'
- settings: JSONB, default {}
- trial_ends_at: datetime, nullable

RELATIONSHIPS:
- owner: FK to User (protected, can transfer)
- members: M2M through OrganizationMembership

INDEXES:
- name (btree)
- slug (unique, btree)
- uen (unique, btree) - Critical for Singapore compliance
- stripe_customer_id (btree)
- created_at (btree)

CONSTRAINTS:
- trial_ends_after_creation: trial_ends_at >= created_at
"""

import uuid
import re
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Singapore UEN Validator
UEN_REGEX = r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$'
UEN_VALIDATOR = RegexValidator(
    regex=UEN_REGEX,
    message='Enter a valid Singapore UEN (e.g., 12345678A, 123456789B, or T12AB1234C)'
)

# GST Registration Number Validator
GST_REGEX = r'^M[0-9]{8}[A-Z]$'
GST_VALIDATOR = RegexValidator(
    regex=GST_REGEX,
    message='Enter a valid GST registration number (format: M########A)'
)


class Organization(models.Model):
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Identity
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text='URL-safe identifier (auto-generated from name)'
    )
    
    # Singapore Compliance
    uen = models.CharField(
        max_length=15,
        unique=True,
        validators=[UEN_VALIDATOR],
        help_text='Unique Entity Number (ACRA registered)'
    )
    is_gst_registered = models.BooleanField(
        default=False,
        help_text='Is the organization registered for GST?'
    )
    gst_reg_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[GST_VALIDATOR],
        help_text='GST registration number (if registered)'
    )
    
    # Billing
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        db_index=True
    )
    billing_email = models.EmailField()
    billing_phone = models.CharField(max_length=20, blank=True, default='')
    billing_address = models.JSONField(
        default=dict,
        blank=True,
        help_text='Structured address: {street, city, postal_code, country}'
    )
    
    # Settings
    timezone = models.CharField(max_length=50, default='Asia/Singapore')
    locale = models.CharField(max_length=10, default='en-SG')
    settings = models.JSONField(default=dict, blank=True)
    
    # Relationships
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='owned_organizations'
    )
    members = models.ManyToManyField(
        'users.User',
        through='OrganizationMembership',
        related_name='organizations'
    )
    
    # Trial
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['uen']),
            models.Index(fields=['stripe_customer_id']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(trial_ends_at__isnull=True) | 
                      models.Q(trial_ends_at__gte=models.F('created_at')),
                name='trial_ends_after_creation'
            ),
            models.CheckConstraint(
                check=models.Q(is_gst_registered=False) | 
                      models.Q(gst_reg_no__isnull=False),
                name='gst_registered_requires_number'
            )
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_trial(self) -> bool:
        if not self.trial_ends_at:
            return False
        return timezone.now() < self.trial_ends_at
    
    @property
    def days_left_in_trial(self) -> int:
        if not self.trial_ends_at:
            return 0
        remaining = self.trial_ends_at - timezone.now()
        return max(0, remaining.days)
    
    def clean(self):
        """Model validation"""
        if self.is_gst_registered and not self.gst_reg_no:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'gst_reg_no': 'GST registration number is required for GST-registered organizations.'
            })
        super().clean()
6.2.3 Organization Membership Model
Python

# apps/organizations/models.py (continued)
"""
OrganizationMembership Model Specification
==========================================
Through model for User-Organization M2M with roles and permissions.

REQUIRED FIELDS:
- id: UUID, auto-generated, immutable
- organization_id: FK to Organization
- user_id: FK to User
- role: str, one of (owner, admin, member, viewer)

OPTIONAL FIELDS:
- permissions: ARRAY[str], cached permission strings
- invited_by_id: FK to User, nullable

CONSTRAINTS:
- UNIQUE(organization_id, user_id) - One membership per user per org
- owner_role_matches_org_owner: If role='owner', user must be org.owner
"""

class OrganizationMembership(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    ROLE_PERMISSIONS = {
        'owner': [
            'org.delete', 'org.transfer', 'org.update',
            'billing.manage', 'members.manage', 'subscription.manage',
            'leads.manage', 'leads.view', 'invoices.view'
        ],
        'admin': [
            'org.update', 'billing.view', 'members.manage',
            'leads.manage', 'leads.view', 'invoices.view'
        ],
        'member': [
            'leads.manage', 'leads.view', 'invoices.view'
        ],
        'viewer': [
            'leads.view', 'invoices.view'
        ],
    }
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )
    permissions = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text='Cached permissions for this membership'
    )
    
    # Audit
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invited_memberships'
    )
    
    class Meta:
        db_table = 'organization_memberships'
        unique_together = [('organization', 'user')]
        indexes = [
            models.Index(fields=['organization', 'user']),
            models.Index(fields=['role']),
            models.Index(fields=['user', 'role']),
        ]
    
    def __str__(self):
        return f'{self.user.email} - {self.organization.name} ({self.role})'
    
    def save(self, *args, **kwargs):
        # Auto-populate permissions from role
        if not self.permissions:
            self.permissions = self.ROLE_PERMISSIONS.get(self.role, [])
        super().save(*args, **kwargs)
    
    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions
6.2.4 Plan Model
Python

# apps/subscriptions/models.py
"""
Plan Model Specification
========================
Subscription plan definitions with Stripe integration.

REQUIRED FIELDS:
- id: UUID, auto-generated, immutable
- name: str, max 100 chars
- sku: str, unique, max 50 chars, format: {plan}-{period}
- billing_period: str, one of (month, year)
- amount_cents: int, positive, smallest currency unit

OPTIONAL FIELDS:
- description: text, blank allowed
- currency: str, 3 chars, default 'SGD'
- features: JSONB, default {}
- limits: JSONB, default {}
- 
