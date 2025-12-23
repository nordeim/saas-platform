Meticulous Planning: Project Architecture Document
Phase 1: Implementation Plan for PAD
Before creating the PAD, I will define and validate the comprehensive structure needed.

1.1 PAD Section Requirements Analysis
Section	Purpose	Criticality	Dependencies
1. Executive Overview	Context, goals, constraints	Foundation	None
2. System Architecture	High-level design, diagrams	Foundation	Section 1
3. Technology Stack	Exact versions, justifications	Reference	Section 2
4. Directory Structure	Complete file/folder layout	Implementation	Section 3
5. Data Model	Complete schema with DDL	Implementation	Section 4
6. API Specification	All endpoints, OpenAPI format	Implementation	Section 5
7. Authentication & Authorization	Security model, RBAC	Implementation	Sections 5, 6
8. Business Logic	State machines, workflows	Implementation	Sections 5, 6, 7
9. Frontend Architecture	Components, state, routing	Implementation	Sections 6, 8
10. Background Tasks	Celery tasks, scheduling	Implementation	Sections 5, 8
11. External Integrations	Stripe, SendGrid, AWS	Implementation	Sections 5, 10
12. Infrastructure	Docker, CI/CD, deployment	Operations	All
13. Testing Strategy	Test types, coverage targets	Quality	All
14. Monitoring & Observability	Logging, metrics, alerts	Operations	Section 12
15. Security & Compliance	PDPA, hardening	Compliance	All
16. Error Handling	Error codes, recovery	Implementation	All
17. Configuration Management	Environment variables	Operations	All
18. Data Seeding & Migration	Initial data, migration scripts	Operations	Section 5
1.2 Diagram Requirements
Diagram Type	Notation	Purpose
System Context (C4 Level 1)	Mermaid	External actors and system boundary
Container Diagram (C4 Level 2)	Mermaid	Major containers and their interactions
Component Diagram (C4 Level 3)	Mermaid	Internal component structure
Entity Relationship Diagram	Mermaid	Database schema relationships
Sequence Diagrams	Mermaid	Key workflows (auth, payment, DSAR)
State Machine Diagrams	Mermaid	Subscription, Invoice, DSAR states
Data Flow Diagram	Mermaid	How data moves through system
Deployment Diagram	Mermaid	Infrastructure topology
1.3 Validation Checklist for PAD
Before considering PAD complete, validate:

 Every model field has: name, type, constraints, indexes, description
 Every API endpoint has: method, path, auth, request schema, response schema, errors
 Every component has: name, props interface, state, behavior, dependencies
 Every task has: signature, parameters, retry policy, idempotency, error handling
 Every configuration has: key, type, default, required, description
 All cross-references are consistent (no orphan references)
 All state transitions are defined and valid
 All error codes are unique and documented
 Security considerations addressed for each component
 PDPA compliance verified for all data handling
Phase 2: PAD Implementation Plan Validation
Critical Path Analysis
text

Section 1 (Executive) 
    → Section 2 (Architecture)
        → Section 3 (Tech Stack)
            → Section 5 (Data Model) ←──────────────────┐
                → Section 6 (API)                       │
                    → Section 7 (Auth)                  │
                        → Section 8 (Business Logic) ───┘
                            → Section 9 (Frontend)
                                → Section 10 (Tasks)
                                    → Section 11 (Integrations)
            → Section 4 (Directory) ───────────────────────┘
Risk Assessment
Risk	Impact	Mitigation
Incomplete data model	High	Start with complete ERD, derive from PRDs
API inconsistency	High	Use OpenAPI schema, generate from models
Frontend-Backend mismatch	Medium	Define TypeScript interfaces from API spec
Missing edge cases	Medium	Define state machines for all entities
Configuration gaps	Low	Enumerate all env vars systematically
Plan Approval
✅ Plan validated and approved for execution

Project Architecture Document: NexusCore v3.1
The Meticulously Pragmatic Synthesis for Singapore Market
Document Version: 1.0.0
Last Updated: December 23, 2025
Status: Authoritative Single Source of Truth
Classification: Internal Development Reference

Table of Contents
Executive Overview
System Architecture
Technology Stack
Directory Structure
Data Model
API Specification
Authentication & Authorization
Business Logic & Workflows
Frontend Architecture
Background Tasks
External Integrations
Infrastructure
Testing Strategy
Monitoring & Observability
Security & Compliance
Error Handling
Configuration Management
Data Seeding & Migration
1. Executive Overview
1.1 Project Identity
Attribute	Value
Project Name	NexusCore
Version	3.1.0
Codename	Meticulously Pragmatic Synthesis
Target Market	Singapore B2B SaaS
Language	English-only
Primary Currency	SGD (Singapore Dollar)
1.2 Business Objectives
Objective	Target	Measurement
Lead Generation	≥5% visitor→CTA conversion	GA4 + custom events
Trial Activation	≥70% signup completion	Funnel analytics
Revenue Capture	≥15% trial→paid in 30 days	Stripe + application
User Retention	≥60% 30-day active	Activity tracking
Webhook Reliability	≥99.9% success	Stripe logs
DSAR Compliance	≤72 hours fulfillment	Workflow tracking
1.3 Technical Excellence Targets
Metric	Target	Validation
Mobile LCP	≤2.5s launch, ≤2.0s 60-day	Lighthouse + RUM
Accessibility	WCAG AA	axe-core + manual
Security	Zero critical vulns	Scanning + pentest
Uptime	≥99.9%	Monitoring
Test Coverage	≥70% critical paths	Codecov
API Latency	P95 <500ms	APM
1.4 Architectural Principles
Principle	Implementation
Idempotency First	All mutating operations use idempotency keys
Compliance by Design	PDPA/IRAS requirements embedded in data model
Database-Level Integrity	GST calculations via PostgreSQL GeneratedField
Graceful Degradation	Circuit breakers, retry with backoff
Observability	Structured logging, distributed tracing
Immutable Audit Trail	All state changes logged to Event model
1.5 Scope Boundaries
In Scope (MVP - 12 Weeks)
Marketing website with Elementra design
User registration and authentication
Organization management with UEN validation
Subscription billing with Stripe + PayNow
GST-compliant invoicing
Lead management
DSAR request processing
Admin dashboard
Out of Scope (Phase 2+)
Multi-language support
Mobile applications
Enterprise SSO (SAML/OIDC)
Advanced analytics
AI features
ERP integrations
2. System Architecture
2.1 System Context Diagram (C4 Level 1)
mermaid

C4Context
    title System Context Diagram - NexusCore v3.1

    Person(customer, "Customer", "Singapore business owner using NexusCore for B2B operations")
    Person(admin, "Administrator", "NexusCore staff managing platform")
    Person(visitor, "Visitor", "Prospective customer browsing marketing site")

    System(nexuscore, "NexusCore Platform", "B2B SaaS marketing and lead management platform")

    System_Ext(stripe, "Stripe", "Payment processing, subscription management")
    System_Ext(sendgrid, "SendGrid", "Transactional email delivery")
    System_Ext(aws_s3, "AWS S3", "Document storage (invoices, exports)")
    System_Ext(ga4, "Google Analytics 4", "Marketing analytics")
    System_Ext(sentry, "Sentry", "Error monitoring")

    Rel(visitor, nexuscore, "Browses marketing pages, submits lead forms")
    Rel(customer, nexuscore, "Manages organization, subscriptions, invoices")
    Rel(admin, nexuscore, "Manages leads, processes DSAR, monitors system")
    
    Rel(nexuscore, stripe, "Processes payments, manages subscriptions", "HTTPS/Webhooks")
    Rel(nexuscore, sendgrid, "Sends transactional emails", "HTTPS")
    Rel(nexuscore, aws_s3, "Stores documents", "HTTPS")
    Rel(nexuscore, ga4, "Sends analytics events", "HTTPS")
    Rel(nexuscore, sentry, "Reports errors", "HTTPS")
2.2 Container Diagram (C4 Level 2)
mermaid

C4Container
    title Container Diagram - NexusCore v3.1

    Person(user, "User", "Customer or Visitor")
    
    Container_Boundary(nexuscore, "NexusCore Platform") {
        Container(nextjs, "Next.js Frontend", "Next.js 14, React 18, TypeScript", "Marketing site and application UI")
        Container(django, "Django API", "Django 6.0, DRF, Python 3.12", "REST API, business logic, authentication")
        Container(celery_worker, "Celery Worker", "Celery 5.x, Python 3.12", "Background task processing")
        Container(celery_beat, "Celery Beat", "Celery 5.x", "Scheduled task orchestration")
        
        ContainerDb(postgres, "PostgreSQL", "PostgreSQL 16", "Primary data store")
        ContainerDb(redis, "Redis", "Redis 7.4", "Cache, session, task broker")
    }

    System_Ext(stripe, "Stripe")
    System_Ext(sendgrid, "SendGrid")
    System_Ext(s3, "AWS S3")

    Rel(user, nextjs, "Uses", "HTTPS")
    Rel(nextjs, django, "API calls", "HTTPS/REST")
    Rel(django, postgres, "Reads/Writes", "TCP/5432")
    Rel(django, redis, "Cache/Session", "TCP/6379")
    Rel(celery_worker, redis, "Task queue", "TCP/6379")
    Rel(celery_worker, postgres, "Reads/Writes", "TCP/5432")
    Rel(celery_beat, redis, "Schedule", "TCP/6379")
    
    Rel(django, stripe, "Payment API", "HTTPS")
    Rel(stripe, django, "Webhooks", "HTTPS")
    Rel(celery_worker, sendgrid, "Send emails", "HTTPS")
    Rel(celery_worker, s3, "Store files", "HTTPS")
2.3 Component Diagram (C4 Level 3) - Django API
mermaid

C4Component
    title Component Diagram - Django API Layer

    Container_Boundary(django, "Django API") {
        Component(api_auth, "Auth API", "DRF ViewSet", "Login, register, password reset")
        Component(api_users, "Users API", "DRF ViewSet", "User profile management")
        Component(api_orgs, "Organizations API", "DRF ViewSet", "Org CRUD, membership")
        Component(api_subs, "Subscriptions API", "DRF ViewSet", "Subscription management")
        Component(api_invoices, "Invoices API", "DRF ViewSet", "Invoice listing, PDF")
        Component(api_leads, "Leads API", "DRF ViewSet", "Lead CRUD, assignment")
        Component(api_dsar, "DSAR API", "DRF ViewSet", "Privacy request handling")
        Component(api_webhooks, "Webhooks API", "DRF ViewSet", "External webhook processing")
        
        Component(svc_auth, "Auth Service", "Python", "Authentication logic")
        Component(svc_billing, "Billing Service", "Python", "Stripe integration, GST")
        Component(svc_email, "Email Service", "Python", "Email composition, sending")
        Component(svc_privacy, "Privacy Service", "Python", "DSAR processing, retention")
        
        Component(models, "Domain Models", "Django ORM", "User, Org, Sub, Invoice, Lead, DSAR")
        Component(middleware, "Middleware", "Django", "CSP, security, rate limiting")
    }

    ContainerDb(postgres, "PostgreSQL")
    ContainerDb(redis, "Redis")
    System_Ext(stripe, "Stripe")

    Rel(api_subs, svc_billing, "Uses")
    Rel(api_dsar, svc_privacy, "Uses")
    Rel(api_auth, svc_auth, "Uses")
    Rel(svc_billing, stripe, "API calls")
    Rel(svc_billing, models, "Reads/Writes")
    Rel(models, postgres, "Persists")
    Rel(svc_auth, redis, "Sessions")
2.4 Data Flow Diagram
mermaid

flowchart TB
    subgraph External["External Systems"]
        Stripe[(Stripe)]
        SendGrid[(SendGrid)]
        S3[(AWS S3)]
    end

    subgraph Frontend["Next.js Frontend"]
        Marketing[Marketing Pages]
        App[Application Pages]
        Components[React Components]
    end

    subgraph API["Django API"]
        REST[REST Endpoints]
        Auth[Auth Middleware]
        Validation[Request Validation]
        Services[Business Services]
    end

    subgraph Workers["Celery Workers"]
        Webhooks[Webhook Processing]
        Emails[Email Tasks]
        Reports[Report Generation]
        Retention[Data Retention]
    end

    subgraph Storage["Data Storage"]
        Postgres[(PostgreSQL)]
        Redis[(Redis)]
    end

    Marketing -->|SSG/ISR| App
    App -->|API Calls| REST
    REST -->|Verify Token| Auth
    Auth -->|Validate| Validation
    Validation -->|Execute| Services
    Services -->|CRUD| Postgres
    Services -->|Cache| Redis
    Services -->|Enqueue| Redis
    
    Redis -->|Consume| Webhooks
    Redis -->|Consume| Emails
    Redis -->|Consume| Reports
    Redis -->|Consume| Retention
    
    Webhooks -->|Process| Stripe
    Emails -->|Send| SendGrid
    Reports -->|Store| S3
    
    Stripe -->|Webhook| REST
2.5 Deployment Architecture
mermaid

flowchart TB
    subgraph Internet["Internet"]
        Users[Users]
        StripeWH[Stripe Webhooks]
    end

    subgraph CDN["Cloudflare CDN"]
        CF[Cloudflare]
    end

    subgraph LB["Load Balancer"]
        ALB[AWS ALB]
    end

    subgraph AppTier["Application Tier (ap-southeast-1)"]
        subgraph ECS["ECS Cluster"]
            Django1[Django Container 1]
            Django2[Django Container 2]
            Next1[Next.js Container 1]
            Next2[Next.js Container 2]
            Celery1[Celery Worker 1]
            Celery2[Celery Worker 2]
            Beat[Celery Beat]
        end
    end

    subgraph DataTier["Data Tier (ap-southeast-1)"]
        RDS[(RDS PostgreSQL)]
        ElastiCache[(ElastiCache Redis)]
        S3[(S3 Bucket)]
    end

    subgraph Monitoring["Monitoring"]
        Sentry[Sentry]
        Prometheus[Prometheus]
        Grafana[Grafana]
    end

    Users --> CF
    CF --> ALB
    StripeWH --> ALB
    ALB --> Django1 & Django2
    ALB --> Next1 & Next2
    
    Django1 & Django2 --> RDS
    Django1 & Django2 --> ElastiCache
    Celery1 & Celery2 --> RDS
    Celery1 & Celery2 --> ElastiCache
    Celery1 & Celery2 --> S3
    Beat --> ElastiCache
    
    Django1 & Django2 --> Sentry
    Django1 & Django2 --> Prometheus
    Prometheus --> Grafana
3. Technology Stack
3.1 Backend Stack
Component	Technology	Version	Justification
Runtime	Python	3.12.x	Django 6.0 minimum requirement
Framework	Django	6.0.x	Native CSP, connection health checks, GeneratedField
API	Django REST Framework	3.15.x	Mature, excellent serialization
Database	PostgreSQL	16.x	GeneratedField support, JSONB, full-text search
Cache/Broker	Redis	7.4.x	Session, cache, Celery broker
Task Queue	Celery	5.4.x	Production-proven async tasks
WSGI	Gunicorn	21.x	Production WSGI server
ASGI	Uvicorn	0.27.x	Async view support
3.2 Frontend Stack
Component	Technology	Version	Justification
Framework	Next.js	14.x	App Router, SSG/ISR, React 18
Language	TypeScript	5.x	Type safety, IDE support
UI Library	React	18.x	Component model, hooks
Styling	Tailwind CSS	3.4.x	Utility-first, design system
State	Zustand	4.x	Lightweight, TypeScript-first
Forms	React Hook Form	7.x	Performance, validation
Validation	Zod	3.x	Runtime validation, TypeScript integration
HTTP Client	Axios	1.x	Interceptors, retry support
3.3 Infrastructure Stack
Component	Technology	Version	Justification
Container	Docker	24.x	Consistent environments
Orchestration	Docker Compose (dev)	2.x	Local development
Orchestration	ECS Fargate (prod)	-	Serverless containers
CI/CD	GitHub Actions	-	Integrated with repository
CDN	Cloudflare	-	DDoS protection, caching
Load Balancer	AWS ALB	-	SSL termination, routing
Storage	AWS S3	-	Document storage
Secrets	AWS Secrets Manager	-	Secure configuration
Monitoring	Prometheus + Grafana	-	Metrics, alerting
Error Tracking	Sentry	-	Error aggregation
Logging	CloudWatch Logs	-	Centralized logging
3.4 Python Dependencies
txt

# requirements.txt - Frozen versions for reproducibility

# Core Framework
Django==6.0.1
djangorestframework==3.15.0
django-cors-headers==4.3.1
django-filter==24.1

# Database
psycopg[binary,pool]==3.1.17

# Cache & Session
django-redis==5.4.0
redis==5.0.1
hiredis==2.3.2

# Task Queue
celery[redis]==5.4.0
django-celery-beat==2.5.0
django-celery-results==2.5.1

# Authentication
djangorestframework-simplejwt==5.3.1
PyJWT==2.8.0

# Storage
boto3==1.34.25
django-storages==1.14.2

# Email
sendgrid==6.11.0

# Payment
stripe==8.0.0

# PDF Generation
weasyprint==61.0

# Utilities
python-dateutil==2.8.2
python-dotenv==1.0.0
pydantic==2.5.3

# Monitoring
sentry-sdk[django,celery]==1.39.1
prometheus-client==0.19.0
django-prometheus==2.3.1

# Security
django-csp==3.8  # Fallback for custom CSP needs

# Development
pytest==8.0.0
pytest-django==4.7.0
pytest-cov==4.1.0
pytest-asyncio==0.23.3
factory-boy==3.3.0
faker==22.0.0
black==24.1.0
ruff==0.1.13
mypy==1.8.0
django-stubs==4.2.7
3.5 Node.js Dependencies
JSON

{
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",
    
    "axios": "1.6.5",
    "zustand": "4.5.0",
    "react-hook-form": "7.49.3",
    "zod": "3.22.4",
    "@hookform/resolvers": "3.3.4",
    
    "@headlessui/react": "1.7.18",
    "@heroicons/react": "2.1.1",
    "clsx": "2.1.0",
    "tailwind-merge": "2.2.0",
    
    "@stripe/stripe-js": "2.4.0",
    "@stripe/react-stripe-js": "2.4.0",
    
    "date-fns": "3.2.0",
    "date-fns-tz": "2.0.0"
  },
  "devDependencies": {
    "tailwindcss": "3.4.1",
    "postcss": "8.4.33",
    "autoprefixer": "10.4.17",
    "@tailwindcss/forms": "0.5.7",
    "@tailwindcss/typography": "0.5.10",
    
    "@types/node": "20.11.5",
    "@types/react": "18.2.48",
    "@types/react-dom": "18.2.18",
    
    "eslint": "8.56.0",
    "eslint-config-next": "14.1.0",
    "prettier": "3.2.4",
    "prettier-plugin-tailwindcss": "0.5.11",
    
    "cypress": "13.6.3",
    "@testing-library/react": "14.1.2",
    "@testing-library/jest-dom": "6.2.0",
    "jest": "29.7.0",
    "jest-environment-jsdom": "29.7.0"
  }
}
4. Directory Structure
4.1 Complete Project Layout
text

nexuscore/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Continuous integration
│   │   ├── cd-staging.yml            # Deploy to staging
│   │   ├── cd-production.yml         # Deploy to production
│   │   └── security-scan.yml         # Security scanning
│   ├── CODEOWNERS
│   └── pull_request_template.md
│
├── backend/                           # Django Application
│   ├── apps/
│   │   ├── __init__.py
│   │   │
│   │   ├── core/                      # Core domain models
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py            # User, UserManager
│   │   │   │   ├── organization.py    # Organization, OrganizationMembership
│   │   │   │   └── mixins.py          # TimestampMixin, UUIDMixin
│   │   │   ├── serializers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   └── organization.py
│   │   │   ├── views/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   └── organization.py
│   │   │   ├── permissions.py
│   │   │   ├── validators.py          # UEN validator
│   │   │   ├── signals.py
│   │   │   ├── managers.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_models.py
│   │   │       ├── test_views.py
│   │   │       └── factories.py
│   │   │
│   │   ├── authentication/            # Auth domain
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── backends.py            # Custom auth backend
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── tokens.py              # JWT handling
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       └── test_auth.py
│   │   │
│   │   ├── subscriptions/             # Subscription domain
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── plan.py
│   │   │   │   └── subscription.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services.py            # Stripe integration logic
│   │   │   ├── constants.py           # Plan SKUs, statuses
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_models.py
│   │   │       ├── test_views.py
│   │   │       └── factories.py
│   │   │
│   │   ├── billing/                   # Billing domain
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   └── invoice.py         # Invoice with GeneratedField GST
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── gst.py             # GST calculation service
│   │   │   │   ├── invoice_pdf.py     # PDF generation
│   │   │   │   └── stripe_sync.py     # Stripe invoice sync
│   │   │   ├── constants.py           # IRAS codes, GST rate
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_gst.py
│   │   │       └── test_invoices.py
│   │   │
│   │   ├── leads/                     # Lead management domain
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── filters.py             # Lead filtering
│   │   │   └── tests/
│   │   │       └── __init__.py
│   │   │
│   │   ├── privacy/                   # PDPA compliance domain
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py              # DSARRequest
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data_export.py     # User data compilation
│   │   │   │   ├── data_deletion.py   # Anonymization logic
│   │   │   │   └── retention.py       # Retention policy enforcement
│   │   │   └── tests/
│   │   │       └── __init__.py
│   │   │
│   │   ├── webhooks/                  # Webhook processing domain
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py              # WebhookEvent
│   │   │   ├── views.py               # Webhook endpoints
│   │   │   ├── handlers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── stripe.py          # Stripe webhook handlers
│   │   │   │   └── base.py            # Base handler class
│   │   │   ├── signature.py           # Signature verification
│   │   │   └── tests/
│   │   │       └── __init__.py
│   │   │
│   │   ├── analytics/                 # Event tracking domain
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py              # Event, IdempotencyRecord
│   │   │   ├── services.py            # Event logging service
│   │   │   └── tests/
│   │   │       └── __init__.py
│   │   │
│   │   └── common/                    # Shared utilities
│   │       ├── __init__.py
│   │       ├── exceptions.py          # Custom exceptions
│   │       ├── pagination.py          # Custom pagination
│   │       ├── throttling.py          # Rate limiting
│   │       ├── mixins.py              # Reusable view mixins
│   │       └── utils.py               # Helper functions
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── urls.py                # API URL routing
│   │       └── schema.py              # OpenAPI schema config
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Base settings
│   │   │   ├── development.py         # Dev overrides
│   │   │   ├── staging.py             # Staging overrides
│   │   │   ├── production.py          # Production overrides
│   │   │   └── test.py                # Test overrides
│   │   ├── urls.py                    # Root URL config
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── celery.py                  # Celery configuration
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── webhooks.py                # Webhook processing tasks
│   │   ├── emails.py                  # Email sending tasks
│   │   ├── billing.py                 # Invoice generation tasks
│   │   ├── privacy.py                 # DSAR processing tasks
│   │   ├── cleanup.py                 # Data retention tasks
│   │   └── scheduled.py               # Celery beat schedule
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── security.py                # Security headers
│   │   ├── rate_limit.py              # Rate limiting
│   │   ├── request_id.py              # Request ID tracking
│   │   └── timing.py                  # Response timing
│   │
│   ├── templates/
│   │   ├── emails/
│   │   │   ├── base.html              # Email base template
│   │   │   ├── welcome.html
│   │   │   ├── password_reset.html
│   │   │   ├── invoice.html
│   │   │   ├── payment_failed.html
│   │   │   ├── dsar_verification.html
│   │   │   └── dsar_complete.html
│   │   ├── invoices/
│   │   │   └── invoice_pdf.html       # PDF invoice template
│   │   └── admin/
│   │       └── base_site.html         # Admin customization
│   │
│   ├── static/
│   │   └── admin/
│   │       └── css/
│   │           └── custom.css         # Admin CSS
│   │
│   ├── fixtures/
│   │   ├── plans.json                 # Plan seed data
│   │   └── test_data.json             # Test fixtures
│   │
│   ├── migrations/                    # Django migrations (generated)
│   │
│   ├── scripts/
│   │   ├── entrypoint.sh              # Docker entrypoint
│   │   ├── wait_for_db.py             # DB readiness check
│   │   └── create_superuser.py        # Admin creation script
│   │
│   ├── manage.py
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                          # Next.js Application
│   ├── app/
│   │   ├── (marketing)/               # Marketing route group
│   │   │   ├── page.tsx               # Homepage
│   │   │   ├── pricing/
│   │   │   │   └── page.tsx
│   │   │   ├── solutions/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [slug]/
│   │   │   │       └── page.tsx
│   │   │   ├── case-studies/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [slug]/
│   │   │   │       └── page.tsx
│   │   │   ├── contact/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx             # Marketing layout
│   │   │
│   │   ├── (auth)/                    # Auth route group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   ├── forgot-password/
│   │   │   │   └── page.tsx
│   │   │   ├── reset-password/
│   │   │   │   └── page.tsx
│   │   │   ├── verify-email/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx             # Auth layout
│   │   │
│   │   ├── (dashboard)/               # Dashboard route group
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── organizations/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── new/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx
│   │   │   │       ├── settings/
│   │   │   │       │   └── page.tsx
│   │   │   │       └── members/
│   │   │   │           └── page.tsx
│   │   │   ├── subscriptions/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   ├── invoices/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   ├── settings/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── profile/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── privacy/
│   │   │   │       └── page.tsx
│   │   │   └── layout.tsx             # Dashboard layout
│   │   │
│   │   ├── api/                       # Next.js API routes (if needed)
│   │   │   └── health/
│   │   │       └── route.ts
│   │   │
│   │   ├── layout.tsx                 # Root layout
│   │   ├── loading.tsx                # Global loading
│   │   ├── error.tsx                  # Global error
│   │   ├── not-found.tsx              # 404 page
│   │   └── globals.css                # Global styles
│   │
│   ├── components/
│   │   ├── ui/                        # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Checkbox.tsx
│   │   │   ├── Radio.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Dropdown.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Toast.tsx
│   │   │   ├── Spinner.tsx
│   │   │   ├── Skeleton.tsx
│   │   │   └── index.ts               # Barrel export
│   │   │
│   │   ├── layout/                    # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Navigation.tsx
│   │   │   ├── MobileNav.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── forms/                     # Form components
│   │   │   ├── ContactForm.tsx
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   ├── OrganizationForm.tsx
│   │   │   ├── PasswordResetForm.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── marketing/                 # Marketing-specific
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   ├── CTA.tsx
│   │   │   ├── PricingCard.tsx
│   │   │   ├── PricingTable.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── dashboard/                 # Dashboard-specific
│   │   │   ├── StatsCard.tsx
│   │   │   ├── ActivityFeed.tsx
│   │   │   ├── SubscriptionCard.tsx
│   │   │   ├── InvoiceTable.tsx
│   │   │   ├── MemberList.tsx
│   │   │   └── index.ts
│   │   │
│   │   └── shared/                    # Shared components
│   │       ├── Logo.tsx
│   │       ├── Avatar.tsx
│   │       ├── EmptyState.tsx
│   │       ├── ErrorBoundary.tsx
│   │       ├── SEO.tsx
│   │       └── index.ts
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts              # Axios instance
│   │   │   ├── auth.ts                # Auth API calls
│   │   │   ├── organizations.ts       # Org API calls
│   │   │   ├── subscriptions.ts       # Sub API calls
│   │   │   ├── invoices.ts            # Invoice API calls
│   │   │   └── types.ts               # API response types
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useOrganization.ts
│   │   │   ├── useSubscription.ts
│   │   │   ├── useToast.ts
│   │   │   ├── useDebounce.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── stores/
│   │   │   ├── auth.ts                # Auth Zustand store
│   │   │   ├── organization.ts        # Org Zustand store
│   │   │   ├── ui.ts                  # UI state store
│   │   │   └── index.ts
│   │   │
│   │   ├── utils/
│   │   │   ├── cn.ts                  # Classname utility
│   │   │   ├── format.ts              # Formatting utilities
│   │   │   ├── validation.ts          # Zod schemas
│   │   │   └── constants.ts           # App constants
│   │   │
│   │   └── stripe.ts                  # Stripe client setup
│   │
│   ├── styles/
│   │   └── tailwind.css               # Tailwind entry
│   │
│   ├── public/
│   │   ├── images/
│   │   │   ├── logo.svg
│   │   │   ├── logo-dark.svg
│   │   │   └── og-image.png
│   │   ├── fonts/
│   │   └── favicon.ico
│   │
│   ├── types/
│   │   ├── api.ts                     # API types
│   │   ├── models.ts                  # Domain model types
│   │   └── global.d.ts                # Global type declarations
│   │
│   ├── .env.local.example
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   ├── package.json
│   ├── Dockerfile
│   └── cypress/
│       ├── e2e/
│       │   ├── auth.cy.ts
│       │   ├── onboarding.cy.ts
│       │   ├── subscription.cy.ts
│       │   └── invoice.cy.ts
│       ├── fixtures/
│       ├── support/
│       └── cypress.config.ts
│
├── infrastructure/
│   ├── docker/
│   │   ├── docker-compose.yml         # Development
│   │   ├── docker-compose.prod.yml    # Production
│   │   ├── nginx/
│   │   │   └── nginx.conf
│   │   └── scripts/
│   │       └── backup.sh
│   │
│   ├── terraform/
│   │   ├── environments/
│   │   │   ├── staging/
│   │   │   │   ├── main.tf
│   │   │   │   └── variables.tf
│   │   │   └── production/
│   │   │       ├── main.tf
│   │   │       └── variables.tf
│   │   └── modules/
│   │       ├── ecs/
│   │       ├── rds/
│   │       ├── elasticache/
│   │       └── s3/
│   │
│   └── scripts/
│       ├── deploy.sh
│       ├── rollback.sh
│       └── health-check.sh
│
├── docs/
│   ├── architecture.md                # This document
│   ├── api-reference.md
│   ├── deployment.md
│   ├── development.md
│   ├── testing.md
│   └── runbooks/
│       ├── incident-response.md
│       ├── database-maintenance.md
│       └── dsar-processing.md
│
├── .gitignore
├── .editorconfig
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── Makefile
5. Data Model
5.1 Entity Relationship Diagram
mermaid

erDiagram
    User ||--o{ OrganizationMembership : "has many"
    User ||--o{ Lead : "assigned"
    User ||--o{ DSARRequest : "requests"
    User ||--o{ Event : "triggers"
    
    Organization ||--o{ OrganizationMembership : "has many"
    Organization ||--|| User : "owned by"
    Organization ||--o{ Subscription : "has many"
    Organization ||--o{ Invoice : "has many"
    Organization ||--o{ Event : "tracks"
    
    Plan ||--o{ Subscription : "defines"
    
    Subscription ||--o{ Invoice : "generates"
    
    WebhookEvent ||--o{ Event : "triggers"
    
    User {
        uuid id PK
        string email UK
        string name
        string company
        string phone
        boolean is_verified
        uuid verification_token
        datetime verification_sent_at
        boolean is_active
        boolean is_staff
        string timezone
        jsonb email_preferences
        datetime created_at
        datetime updated_at
        datetime last_login
    }
    
    Organization {
        uuid id PK
        string name
        string slug UK
        string uen UK
        boolean is_gst_registered
        string gst_reg_no
        string stripe_customer_id
        string billing_email
        string billing_phone
        jsonb billing_address
        string timezone
        string locale
        jsonb settings
        uuid owner_id FK
        datetime created_at
        datetime updated_at
        datetime trial_ends_at
    }
    
    OrganizationMembership {
        uuid id PK
        uuid organization_id FK
        uuid user_id FK
        string role
        array permissions
        datetime joined_at
        uuid invited_by FK
    }
    
    Plan {
        uuid id PK
        string name
        string description
        string sku UK
        string billing_period
        bigint amount_cents
        string currency
        jsonb features
        jsonb limits
        boolean is_active
        boolean is_visible
        int display_order
        string stripe_price_id
        string stripe_product_id
        datetime created_at
        datetime updated_at
    }
    
    Subscription {
        uuid id PK
        uuid organization_id FK
        uuid plan_id FK
        string status
        boolean cancel_at_period_end
        datetime current_period_start
        datetime current_period_end
        datetime trial_start
        datetime trial_end
        string stripe_subscription_id UK
        string stripe_customer_id
        string stripe_latest_invoice_id
        jsonb metadata
        datetime created_at
        datetime updated_at
        datetime canceled_at
    }
    
    Invoice {
        uuid id PK
        uuid subscription_id FK
        uuid organization_id FK
        bigint subtotal_cents
        decimal gst_rate
        bigint gst_amount_cents "GENERATED"
        bigint total_amount_cents "GENERATED"
        bigint amount_paid_cents
        string currency
        string iras_transaction_code
        string status
        boolean paid
        datetime created_at
        datetime due_date
        datetime paid_at
        string pdf_url
        string stripe_invoice_id UK
        string stripe_payment_intent_id
        jsonb line_items
        jsonb metadata
    }
    
    Lead {
        uuid id PK
        string name
        string email
        string phone
        string company
        string job_title
        string source
        string status
        text notes
        string utm_source
        string utm_medium
        string utm_campaign
        string utm_term
        string utm_content
        jsonb form_data
        uuid assigned_to FK
        datetime next_follow_up
        uuid converted_to_user FK
        datetime converted_at
        datetime created_at
        datetime updated_at
    }
    
    DSARRequest {
        uuid id PK
        string user_email
        uuid user_id FK
        string request_type
        string status
        uuid verification_token
        datetime verified_at
        string verification_method
        string export_url
        datetime export_expires_at
        jsonb metadata
        text failure_reason
        datetime requested_at
        datetime processing_started_at
        datetime processed_at
        uuid deletion_approved_by FK
        datetime deletion_approved_at
    }
    
    Event {
        uuid id PK
        string event_type
        uuid user_id FK
        uuid organization_id FK
        jsonb data
        datetime created_at
    }
    
    IdempotencyRecord {
        uuid id PK
        string key UK
        string request_path
        string request_method
        string request_hash
        string status
        int response_status_code
        jsonb response_body
        datetime created_at
        datetime updated_at
        datetime expires_at
    }
    
    WebhookEvent {
        uuid id PK
        string service
        string event_id UK
        string event_type
        jsonb payload
        boolean processed
        text processing_error
        int retry_count
        datetime last_retry_at
        datetime created_at
        datetime processed_at
    }
5.2 Complete Model Specifications
5.2.1 User Model
Python

# backend/apps/core/models/user.py

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.validators import EmailValidator
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom user manager for email-based authentication.
    """
    
    def create_user(self, email: str, password: str = None, **extra_fields) -> 'User':
        """
        Create and return a regular user with email and password.
        
        Args:
            email: User's email address (required, unique)
            password: User's password (optional, will be unusable if not provided)
            **extra_fields: Additional user fields
            
        Returns:
            User: Created user instance
            
        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email: str, password: str, **extra_fields) -> 'User':
        """
        Create and return a superuser.
        
        Args:
            email: Superuser's email address
            password: Superuser's password (required)
            **extra_fields: Additional user fields
            
        Returns:
            User: Created superuser instance
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
    
    def get_by_natural_key(self, email: str) -> 'User':
        """Get user by email (case-insensitive)."""
        return self.get(email__iexact=email)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email-based authentication.
    
    Attributes:
        id: UUID primary key
        email: Unique email address (login identifier)
        name: Full name for display
        company: Company name (optional)
        phone: Phone number (optional)
        is_verified: Email verification status
        verification_token: Token for email verification
        verification_sent_at: When verification email was sent
        is_active: Account active status
        is_staff: Admin access
        timezone: User's timezone (default: Asia/Singapore)
        email_preferences: JSON preferences for email notifications
        created_at: Account creation timestamp
        updated_at: Last modification timestamp
        last_login: Last successful login
    """
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the user"
    )
    
    # Core fields
    email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[EmailValidator()],
        help_text="Primary email address and login identifier"
    )
    name = models.CharField(
        max_length=255,
        help_text="Full name for display"
    )
    company = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Company or organization name"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text="Phone number with country code"
    )
    
    # Verification
    is_verified = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether email has been verified"
    )
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text="Token for email verification link"
    )
    verification_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When verification email was last sent"
    )
    
    # Permissions
    is_active = models.BooleanField(
        default=True,
        help_text="Whether account is active"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Whether user can access admin site"
    )
    
    # Preferences
    timezone = models.CharField(
        max_length=50,
        default='Asia/Singapore',
        help_text="User's preferred timezone"
    )
    email_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Email notification preferences"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When account was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When account was last modified"
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last successful login"
    )
    
    # Manager
    objects = UserManager()
    
    # Auth configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email'], name='idx_users_email'),
            models.Index(fields=['created_at'], name='idx_users_created'),
            models.Index(
                fields=['is_verified', 'is_active'],
                name='idx_users_verified_active'
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(is_verified=False) | models.Q(is_active=True),
                name='verified_users_must_be_active',
                violation_error_message="Verified users must be active"
            ),
        ]
    
    def __str__(self) -> str:
        return self.email
    
    def get_full_name(self) -> str:
        """Return user's full name."""
        return self.name
    
    def get_short_name(self) -> str:
        """Return user's first name."""
        return self.name.split()[0] if self.name else ''
    
    def regenerate_verification_token(self) -> None:
        """Generate new verification token and update sent timestamp."""
        self.verification_token = uuid.uuid4()
        self.verification_sent_at = timezone.now()
        self.save(update_fields=['verification_token', 'verification_sent_at'])
    
    def verify_email(self) -> None:
        """Mark email as verified."""
        self.is_verified = True
        self.save(update_fields=['is_verified', 'updated_at'])
    
    @property
    def can_resend_verification(self) -> bool:
        """Check if verification email can be resent (5 min cooldown)."""
        if not self.verification_sent_at:
            return True
        cooldown = timezone.timedelta(minutes=5)
        return timezone.now() > self.verification_sent_at + cooldown
5.2.2 Organization Model
Python

# backend/apps/core/models/organization.py

import uuid
import re
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_uen(value: str) -> None:
    """
    Validate Singapore Unique Entity Number (UEN).
    
    Valid formats:
    - Business (ROB): NNNNNNNNX (8 digits + 1 letter)
    - Local Company (ROC): NNNNNNNNNX (9 digits + 1 letter)
    - Others: TNNXXXXXXXXX (T/S/R/Q + 2 digits + 2 chars + 5 chars)
    
    Args:
        value: UEN string to validate
        
    Raises:
        ValidationError: If UEN format is invalid
    """
    patterns = [
        r'^[0-9]{8}[A-Z]$',           # Business (ROB)
        r'^[0-9]{9}[A-Z]$',           # Local Company (ROC)
        r'^[TSRQ][0-9]{2}[A-Z]{2}[0-9]{4}[A-Z]$',  # Other entities
    ]
    
    if not any(re.match(pattern, value.upper()) for pattern in patterns):
        raise ValidationError(
            f"'{value}' is not a valid Singapore UEN. "
            "Expected formats: 12345678A, 123456789B, or T12AB1234C"
        )


def validate_gst_registration(value: str) -> None:
    """
    Validate Singapore GST Registration Number.
    
    Format: M + 8 digits + 1 letter (e.g., M12345678A)
    
    Args:
        value: GST registration number to validate
        
    Raises:
        ValidationError: If format is invalid
    """
    pattern = r'^M[0-9]{8}[A-Z]$'
    if not re.match(pattern, value.upper()):
        raise ValidationError(
            f"'{value}' is not a valid GST registration number. "
            "Expected format: M12345678A"
        )


class Organization(models.Model):
    """
    Company/Organization entity with Singapore compliance fields.
    
    Attributes:
        id: UUID primary key
        name: Organization display name
        slug: URL-safe identifier
        uen: Singapore Unique Entity Number
        is_gst_registered: GST registration status
        gst_reg_no: GST registration number (if registered)
        stripe_customer_id: Stripe customer ID
        billing_email: Primary billing contact
        billing_phone: Billing phone number
        billing_address: Structured billing address
        timezone: Organization timezone
        locale: Locale for formatting
        settings: Flexible settings storage
        owner: Owner user reference
        created_at: Creation timestamp
        updated_at: Modification timestamp
        trial_ends_at: Trial period end date
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Identity
    name = models.CharField(
        max_length=255,
        help_text="Organization display name"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="URL-safe identifier"
    )
    
    # Singapore Compliance
    uen = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        validators=[validate_uen],
        help_text="Singapore Unique Entity Number (ACRA registered)"
    )
    is_gst_registered = models.BooleanField(
        default=False,
        help_text="Whether organization is GST registered"
    )
    gst_reg_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[validate_gst_registration],
        help_text="GST registration number (required if GST registered)"
    )
    
    # Billing
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        db_index=True,
        help_text="Stripe customer ID for billing"
    )
    billing_email = models.EmailField(
        help_text="Primary billing contact email"
    )
    billing_phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text="Billing contact phone"
    )
    billing_address = models.JSONField(
        default=dict,
        blank=True,
        help_text="Structured billing address (line1, line2, city, postal_code, country)"
    )
    
    # Settings
    timezone = models.CharField(
        max_length=50,
        default='Asia/Singapore'
    )
    locale = models.CharField(
        max_length=10,
        default='en-SG'
    )
    settings = models.JSONField(
        default=dict,
        blank=True,
        help_text="Flexible settings storage"
    )
    
    # Relationships
    owner = models.ForeignKey(
        'core.User',
        on_delete=models.PROTECT,
        related_name='owned_organizations',
        help_text="Organization owner"
    )
    members = models.ManyToManyField(
        'core.User',
        through='OrganizationMembership',
        related_name='organizations'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trial_ends_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When trial period ends"
    )
    
    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'], name='idx_orgs_name'),
            models.Index(fields=['slug'], name='idx_orgs_slug'),
            models.Index(fields=['uen'], name='idx_orgs_uen'),
            models.Index(fields=['stripe_customer_id'], name='idx_orgs_stripe'),
            models.Index(fields=['created_at'], name='idx_orgs_created'),
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
            ),
        ]
    
    def __str__(self) -> str:
        return self.name
    
    def clean(self) -> None:
        """Validate model constraints."""
        super().clean()
        
        # Ensure GST number is provided if registered
        if self.is_gst_registered and not self.gst_reg_no:
            raise ValidationError({
                'gst_reg_no': 'GST registration number is required when GST registered.'
            })
        
        # Clear GST number if not registered
        if not self.is_gst_registered:
            self.gst_reg_no = None
    
    @property
    def is_in_trial(self) -> bool:
        """Check if organization is in trial period."""
        if not self.trial_ends_at:
            return False
        return timezone.now() < self.trial_ends_at
    
    @property
    def days_left_in_trial(self) -> int:
        """Calculate days remaining in trial."""
        if not self.trial_ends_at:
            return 0
        remaining = self.trial_ends_at - timezone.now()
        return max(0, remaining.days)
    
    @property
    def gst_rate(self) -> float:
        """Return applicable GST rate."""
        return 0.09 if self.is_gst_registered else 0.0


class OrganizationMembership(models.Model):
    """
    Organization membership with role-based access.
    
    Roles:
        - owner: Full access, can delete organization
        - admin: Can manage members and settings
        - member: Can view and create resources
        - viewer: Read-only access
    """
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    # Role -> Default permissions mapping
    DEFAULT_PERMISSIONS = {
        'owner': [
            'org:delete', 'org:update', 'org:read',
            'member:create', 'member:update', 'member:delete', 'member:read',
            'subscription:create', 'subscription:update', 'subscription:cancel', 'subscription:read',
            'invoice:read', 'invoice:download',
        ],
        'admin': [
            'org:update', 'org:read',
            'member:create', 'member:update', 'member:delete', 'member:read',
            'subscription:read', 'subscription:update',
            'invoice:read', 'invoice:download',
        ],
        'member': [
            'org:read',
            'member:read',
            'subscription:read',
            'invoice:read', 'invoice:download',
        ],
        'viewer': [
            'org:read',
            'member:read',
            'subscription:read',
            'invoice:read',
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
        'core.User',
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member',
        db_index=True
    )
    permissions = models.JSONField(
        default=list,
        blank=True,
        help_text="Explicit permissions (overrides role defaults if set)"
    )
    
    # Audit
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_invitations'
    )
    
    class Meta:
        db_table = 'organization_memberships'
        verbose_name = 'Organization Membership'
        verbose_name_plural = 'Organization Memberships'
        unique_together = [('organization', 'user')]
        indexes = [
            models.Index(
                fields=['organization', 'user'],
                name='idx_membership_org_user'
            ),
            models.Index(fields=['role'], name='idx_membership_role'),
        ]
    
    def __str__(self) -> str:
        return f"{self.user.email} - {self.organization.name} ({self.role})"
    
    def save(self, *args, **kwargs):
        """Set default permissions based on role if not explicitly set."""
        if not self.permissions:
            self.permissions = self.DEFAULT_PERMISSIONS.get(self.role, [])
        super().save(*args, **kwargs)
    
    def has_permission(self, permission: str) -> bool:
        """Check if membership has a specific permission."""
        effective_permissions = self.permissions or self.DEFAULT_PERMISSIONS.get(self.role, [])
        return permission in effective_permissions
    
    def get_effective_permissions(self) -> list:
        """Get all effective permissions for this membership."""
        return self.permissions or self.DEFAULT_PERMISSIONS.get(self.role, [])
5.2.3 Subscription Models
Python

# backend/apps/subscriptions/models/plan.py

import uuid
from django.db import models
from django.core.validators import MinValueValidator


class Plan(models.Model):
    """
    Subscription plan definition.
    
    Plans are synchronized with Stripe Products/Prices.
    """
    
    BILLING_PERIOD_CHOICES = [
        ('month', 'Monthly'),
        ('year', 'Annual'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Identity
    name = models.CharField(
        max_length=100,
        help_text="Display name (e.g., 'Starter', 'Pro')"
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text="Plan description for marketing"
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique SKU (e.g., 'starter-month', 'pro-year')"
    )
    
    # Pricing
    billing_period = models.CharField(
        max_length=10,
        choices=BILLING_PERIOD_CHOICES,
        default='month'
    )
    amount_cents = models.PositiveBigIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Price in cents (SGD)"
    )
    currency = models.CharField(
        max_length=3,
        default='SGD'
    )
    
    # Features
    features = models.JSONField(
        default=dict,
        blank=True,
        help_text="Feature flags and descriptions"
    )
    limits = models.JSONField(
        default=dict,
        blank=True,
        help_text="Resource limits (users, storage, etc.)"
    )
    
    # Display
    is_active = models.BooleanField(
        default=True,
        help_text="Whether plan can be selected"
    )
    is_visible = models.BooleanField(
        default=True,
        help_text="Whether plan is shown on pricing page"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in pricing table"
    )
    is_popular = models.BooleanField(
        default=False,
        help_text="Highlight as most popular"
    )
    
    # Trial
    trial_days = models.PositiveIntegerField(
        default=14,
        help_text="Free trial duration in days"
    )
    
    # Stripe integration
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        help_text="Stripe Product ID"
    )
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        db_index=True,
        help_text="Stripe Price ID"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plans'
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'
        ordering = ['display_order', 'created_at']
        indexes = [
            models.Index(fields=['sku'], name='idx_plans_sku'),
            models.Index(
                fields=['is_active', 'is_visible'],
                name='idx_plans_active_visible'
            ),
            models.Index(fields=['stripe_price_id'], name='idx_plans_stripe'),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} ({self.billing_period})"
    
    @property
    def amount_dollars(self) -> float:
        """Amount in dollars (SGD)."""
        return self.amount_cents / 100
    
    @property
    def monthly_equivalent_cents(self) -> int:
        """Monthly equivalent price for comparison."""
        if self.billing_period == 'year':
            return self.amount_cents // 12
        return self.amount_cents
    
    def get_feature_list(self) -> list:
        """Get features as a list for display."""
        return self.features.get('list', [])


# backend/apps/subscriptions/models/subscription.py

class Subscription(models.Model):
    """
    Customer subscription state.
    
    State machine:
        trialing -> active -> canceled
        trialing -> canceled
        active -> past_due -> active
        active -> past_due -> canceled
        active -> unpaid -> canceled
    """
    
    STATUS_CHOICES = [
        ('trialing', 'Trialing'),
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('unpaid', 'Unpaid'),
    ]
    
    # Valid status transitions
    VALID_TRANSITIONS = {
        'trialing': ['active', 'canceled'],
        'active': ['past_due', 'canceled', 'unpaid'],
        'past_due': ['active', 'canceled', 'unpaid'],
        'unpaid': ['active', 'canceled'],
        'canceled': [],  # Terminal state
    }
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    organization = models.ForeignKey(
        'core.Organization',
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='trialing',
        db_index=True
    )
    cancel_at_period_end = models.BooleanField(
        default=False,
        help_text="Cancel at end of billing period"
    )
    
    # Billing period
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    
    # Trial
    trial_start = models.DateTimeField(
        null=True,
        blank=True
    )
    trial_end = models.DateTimeField(
        null=True,
        blank=True
    )
    
    # Stripe integration
    stripe_subscription_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        db_index=True
    )
    stripe_latest_invoice_id = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    
    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    canceled_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created_at']
        indexes = [
            models.Index(
                fields=['organization', 'status'],
                name='idx_subs_org_status'
            ),
            models.Index(
                fields=['status', 'current_period_end'],
                name='idx_subs_status_period'
            ),
            models.Index(
                fields=['stripe_subscription_id'],
                name='idx_subs_stripe'
            ),
            # Partial index for active subscriptions
            models.Index(
                fields=['organization'],
                condition=models.Q(status__in=['active', 'trialing']),
                name='idx_subs_active'
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(current_period_end__gt=models.F('current_period_start')),
                name='period_end_after_start'
            ),
            models.CheckConstraint(
                check=~models.Q(status='trialing') | models.Q(trial_end__isnull=False),
                name='trial_status_requires_trial_end'
            ),
        ]
    
    def __str__(self) -> str:
        return f"{self.organization.name} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is active or trialing."""
        return self.status in ['active', 'trialing']
    
    @property
    def is_in_trial(self) -> bool:
        """Check if in trial period."""
        if not self.trial_end:
            return False
        return timezone.now() < self.trial_end and self.status == 'trialing'
    
    @property
    def days_until_renewal(self) -> int:
        """Days until subscription renews."""
        remaining = self.current_period_end - timezone.now()
        return max(0, remaining.days)
    
    def can_transition_to(self, new_status: str) -> bool:
        """Check if status transition is valid."""
        return new_status in self.VALID_TRANSITIONS.get(self.status, [])
    
    def transition_to(self, new_status: str) -> None:
        """
        Transition to a new status.
        
        Raises:
            ValueError: If transition is invalid
        """
        if not self.can_transition_to(new_status):
            raise ValueError(
                f"Cannot transition from '{self.status}' to '{new_status}'"
            )
        
        old_status = self.status
        self.status = new_status
        
        if new_status == 'canceled':
            self.canceled_at = timezone.now()
        
        self.save(update_fields=['status', 'canceled_at', 'updated_at'])
        
        # Log state transition
        from apps.analytics.models import Event
        Event.objects.create(
            event_type='subscription_status_changed',
            organization=self.organization,
            data={
                'subscription_id': str(self.id),
                'old_status': old_status,
                'new_status': new_status,
            }
        )
5.2.4 Invoice Model (with GST GeneratedField)
Python

# backend/apps/billing/models/invoice.py

import uuid
from decimal import Decimal
from django.db import models
from django.db.models import F
from django.db.models.functions import Round
from django.utils import timezone

from apps.billing.constants import IRAS_TRANSACTION_CODES, GST_RATE


class Invoice(models.Model):
    """
    GST-compliant invoice with database-level calculations.
    
    Uses Django 6.0 GeneratedField for GST calculations to ensure:
    - Consistent calculations across all database access patterns
    - No floating-point precision errors
    - Audit-ready immutable calculations
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('uncollectible', 'Uncollectible'),
    ]
    
    IRAS_CODE_CHOICES = [
        ('SR', 'Standard Rate'),
        ('ZR', 'Zero Rate'),
        ('OS', 'Out of Scope'),
        ('ES', 'Exempt Supply'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    organization = models.ForeignKey(
        'core.Organization',
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    subscription = models.ForeignKey(
        'subscriptions.Subscription',
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,
        blank=True
    )
    
    # Amounts (stored in cents to avoid floating-point issues)
    subtotal_cents = models.BigIntegerField(
        help_text="Net amount before tax in cents"
    )
    
    # GST Configuration
    gst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=Decimal('0.0900'),
        help_text="GST rate (0.0900 = 9%)"
    )
    
    # DJANGO 6.0 FEATURE: Database-computed GST Amount
    # This ensures GST is always calculated correctly at the database level
    gst_amount_cents = models.GeneratedField(
        expression=Round(
            F('subtotal_cents') * F('gst_rate'),
            output_field=models.BigIntegerField()
        ),
        output_field=models.BigIntegerField(),
        db_persist=True,
        help_text="GST amount in cents (database-computed)"
    )
    
    # DJANGO 6.0 FEATURE: Database-computed Total
    total_amount_cents = models.GeneratedField(
        expression=F('subtotal_cents') + Round(
            F('subtotal_cents') * F('gst_rate'),
            output_field=models.BigIntegerField()
        ),
        output_field=models.BigIntegerField(),
        db_persist=True,
        help_text="Total amount in cents (database-computed)"
    )
    
    # Payment tracking
    amount_paid_cents = models.BigIntegerField(
        default=0,
        help_text="Amount paid in cents"
    )
    currency = models.CharField(
        max_length=3,
        default='SGD'
    )
    
    # IRAS Compliance
    iras_transaction_code = models.CharField(
        max_length=10,
        choices=IRAS_CODE_CHOICES,
        default='SR',
        help_text="IRAS transaction type code"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )
    paid = models.BooleanField(
        default=False,
        db_index=True
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    # Documents
    pdf_url = models.URLField(
        blank=True,
        default='',
        help_text="S3 URL for generated PDF"
    )
    
    # Stripe integration
    stripe_invoice_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    
    # Line items
    line_items = models.JSONField(
        default=list,
        blank=True,
        help_text="Invoice line items"
    )
    
    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True
    )
    
    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-created_at']
        indexes = [
            models.Index(
                fields=['organization', 'status'],
                name='idx_invoices_org_status'
            ),
            models.Index(
                fields=['status', 'due_date'],
                name='idx_invoices_status_due'
            ),
            models.Index(
                fields=['stripe_invoice_id'],
                name='idx_invoices_stripe'
            ),
            models.Index(
                fields=['created_at'],
                name='idx_invoices_created'
            ),
            # Partial index for overdue invoices
            models.Index(
                fields=['due_date'],
                condition=models.Q(status='open'),
                name='idx_invoices_overdue'
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount_paid_cents__lte=F('subtotal_cents') + 
                              Round(F('subtotal_cents') * F('gst_rate'))),
                name='amount_paid_not_exceed_total'
            ),
            models.CheckConstraint(
                check=~models.Q(paid=True) | models.Q(paid_at__isnull=False),
                name='paid_invoices_require_paid_at'
            ),
        ]
    
    def __str__(self) -> str:
        return 
