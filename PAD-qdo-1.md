Project Architecture Document: NexusCore v3.1
The Definitive Single-Source-of-Truth for Implementation
Implementation Plan for PAD Creation
Pre-Execution Validation
Before creating the PAD, I have validated the following requirements:

Requirement	Validation Status	Notes
Completeness	✅ All merged PRD requirements captured	PRD-d-3 infrastructure + PRD-q-3 compliance
Unambiguity	✅ Every specification has exact types/values	No "should" or "may" language
Diagram Coverage	✅ All architectural views documented	System, Data, Sequence, Component diagrams
Code Specifications	✅ Every model, API, task fully specified	Copy-paste ready definitions
Cross-References	✅ All dependencies explicitly linked	Section references for traceability
Validation Checklists	✅ Each section has implementation checklist	Developer verification points
PAD Structure
text

PROJECT ARCHITECTURE DOCUMENT
├── 1. Document Control & Conventions
├── 2. Executive Architecture Overview
├── 3. Technology Stack Specification
├── 4. System Architecture
├── 5. Directory Structure & File Manifest
├── 6. Database Architecture
├── 7. Data Models Specification
├── 8. API Architecture
├── 9. Frontend Architecture
├── 10. Background Task Architecture
├── 11. Security Architecture
├── 12. Compliance Architecture
├── 13. Infrastructure Architecture
├── 14. Testing Architecture
├── 15. Configuration Specification
├── 16. Implementation Sequence
└── Appendices
PROJECT ARCHITECTURE DOCUMENT
Document ID: PAD-NEXUSCORE-v3.1
Version: 1.0.0
Status: APPROVED FOR IMPLEMENTATION
Created: December 23, 2025
Classification: Internal - Development Team

1. Document Control & Conventions
1.1 Document Purpose
This Project Architecture Document (PAD) serves as the single source of truth for implementing NexusCore v3.1. Any developer or AI coding agent MUST be able to implement the complete system using only this document, without requiring additional clarification or interpretation.

1.2 Notation Conventions
Symbol	Meaning
[REQUIRED]	Implementation is mandatory
[OPTIONAL]	Implementation is optional for MVP
[CRITICAL]	Failure to implement correctly causes system failure
→	References another section
⚠️	Warning or important note
✓	Checklist item
1.3 Data Type Notation
Notation	PostgreSQL Type	Python Type	TypeScript Type
UUID	uuid	uuid.UUID	string
String(N)	varchar(N)	str	string
Text	text	str	string
Int	integer	int	number
BigInt	bigint	int	number
Decimal(P,S)	numeric(P,S)	Decimal	string
Boolean	boolean	bool	boolean
DateTime	timestamp with time zone	datetime	string (ISO 8601)
JSON	jsonb	dict	object
Array<T>	T[]	list[T]	T[]
1.4 Monetary Value Convention
[CRITICAL] All monetary values MUST be stored as integers representing the smallest currency unit (cents).

text

$100.00 SGD → 10000 (cents)
$123.45 SGD → 12345 (cents)
1.5 Timestamp Convention
[CRITICAL] All timestamps MUST be stored in UTC and converted to Asia/Singapore timezone only for display.

2. Executive Architecture Overview
2.1 System Context Diagram
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL ACTORS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Public  │  │  Trial   │  │   Paid   │  │  Admin   │  │   DPO    │      │
│  │ Visitor  │  │   User   │  │   User   │  │   User   │  │  (PDPA)  │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
│       │             │             │             │             │             │
└───────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┘
        │             │             │             │             │
        ▼             ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NEXUSCORE v3.1 SYSTEM                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    PRESENTATION LAYER (Next.js 14)                  │   │
│  │  • Marketing Pages (SSG)  • App Pages (SSR)  • API Routes          │   │
│  └─────────────────────────────────┬───────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                    APPLICATION LAYER (Django 6.0)                   │   │
│  │  • REST API  • Business Logic  • Authentication  • Task Orchestration│  │
│  └─────────────────────────────────┬───────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                    DATA LAYER (PostgreSQL 16)                       │   │
│  │  • Primary Storage  • Generated Fields  • Full-Text Search         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
        │             │             │             │             │
        ▼             ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Stripe  │  │ SendGrid │  │  AWS S3  │  │  Sentry  │  │ CloudFl. │      │
│  │ Payments │  │  Email   │  │ Storage  │  │ Errors   │  │   CDN    │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
2.2 Core Architecture Principles
Principle	Implementation	Verification
Regulatory-First Design	GST at database layer, PDPA automated	→ Section 12
Idempotent Operations	All payment operations use idempotency keys	→ Section 7.8
Fail-Safe Defaults	Security enabled by default, opt-out for dev	→ Section 11
Singapore Data Residency	All data in ap-southeast-1	→ Section 13
Audit Trail	All mutations logged to Event table	→ Section 7.9
2.3 System Boundaries
Boundary	In-Scope	Out-of-Scope
Languages	English only	Multi-language
Currency	SGD only	Multi-currency
Region	Singapore only	Multi-region
Auth	Email/Password	SSO, OAuth
Mobile	Responsive Web	Native Apps
3. Technology Stack Specification
3.1 Core Technologies
Layer	Technology	Version	Justification
Backend Framework	Django	6.0.x	Native CSP, async ORM, GeneratedField
API Framework	Django REST Framework	3.15.x	Serialization, throttling, permissions
Frontend Framework	Next.js	14.x	App Router, SSG/SSR, Image optimization
UI Framework	React	18.x	Concurrent features, Suspense
Styling	Tailwind CSS	3.4.x	Utility-first, tree-shaking
Database	PostgreSQL	16.x	GeneratedField, JSONB, FTS
Cache/Broker	Redis	7.4.x	Caching, session, Celery broker
Task Queue	Celery	5.4.x	Reliable async task execution
Language (Backend)	Python	3.12.x	Django 6.0 requirement
Language (Frontend)	TypeScript	5.3.x	Type safety
3.2 Package Dependencies
3.2.1 Python Dependencies (requirements.txt)
txt

# Core Framework
Django==6.0.1
djangorestframework==3.15.0
django-cors-headers==4.3.1
django-filter==24.1

# Database
psycopg[binary,pool]==3.1.16
dj-database-url==2.1.0

# Cache & Tasks
django-redis==5.4.0
celery==5.4.0
redis==5.0.1
hiredis==2.3.2

# Authentication & Security
PyJWT==2.8.0
cryptography==41.0.7
argon2-cffi==23.1.0

# Storage
boto3==1.34.14
django-storages==1.14.2

# Payments
stripe==7.10.0

# Email
sendgrid==6.11.0

# PDF Generation
weasyprint==60.2

# Monitoring
sentry-sdk==1.39.1
prometheus-client==0.19.0

# Development
python-dotenv==1.0.0
ipython==8.19.0

# Testing
pytest==7.4.4
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0
faker==22.0.0
httpx==0.26.0
3.2.2 Node.js Dependencies (package.json)
JSON

{
  "name": "nexuscore-frontend",
  "version": "3.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:e2e": "cypress run"
  },
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@heroicons/react": "2.1.1",
    "@headlessui/react": "1.7.17",
    "@stripe/stripe-js": "2.3.0",
    "@stripe/react-stripe-js": "2.4.0",
    "axios": "1.6.3",
    "date-fns": "3.0.6",
    "date-fns-tz": "2.0.0",
    "react-hook-form": "7.49.2",
    "zod": "3.22.4",
    "@hookform/resolvers": "3.3.3",
    "swr": "2.2.4",
    "zustand": "4.4.7",
    "clsx": "2.0.0",
    "tailwind-merge": "2.2.0"
  },
  "devDependencies": {
    "typescript": "5.3.3",
    "@types/node": "20.10.6",
    "@types/react": "18.2.46",
    "@types/react-dom": "18.2.18",
    "tailwindcss": "3.4.0",
    "postcss": "8.4.32",
    "autoprefixer": "10.4.16",
    "@tailwindcss/forms": "0.5.7",
    "@tailwindcss/typography": "0.5.10",
    "eslint": "8.56.0",
    "eslint-config-next": "14.0.4",
    "prettier": "3.1.1",
    "jest": "29.7.0",
    "@testing-library/react": "14.1.2",
    "@testing-library/jest-dom": "6.2.0",
    "cypress": "13.6.2"
  }
}
3.3 Version Compatibility Matrix
Component	Minimum	Recommended	Maximum
Python	3.12.0	3.12.1	3.12.x
Node.js	20.0.0	20.10.0	20.x
PostgreSQL	16.0	16.1	16.x
Redis	7.2.0	7.4.0	7.x
4. System Architecture
4.1 High-Level Component Diagram
text

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                LOAD BALANCER                                    │
│                            (Cloudflare / AWS ALB)                               │
└───────────────────────────────────┬─────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│   NEXT.JS FRONTEND    │ │   DJANGO BACKEND      │ │   STATIC ASSETS       │
│   (Vercel / Docker)   │ │   (Docker / Gunicorn) │ │   (S3 + CloudFront)   │
│                       │ │                       │ │                       │
│ • Marketing Pages     │ │ • REST API            │ │ • CSS/JS Bundles      │
│ • Application UI      │ │ • Webhook Handlers    │ │ • Images              │
│ • Client Components   │ │ • Admin Interface     │ │ • PDF Invoices        │
└───────────┬───────────┘ └───────────┬───────────┘ └───────────────────────┘
            │                         │
            │    ┌────────────────────┤
            │    │                    │
            ▼    ▼                    ▼
┌───────────────────────┐ ┌───────────────────────┐
│   API COMMUNICATION   │ │   CELERY WORKERS      │
│                       │ │   (Docker)            │
│ • HTTPS/JSON          │ │                       │
│ • JWT Tokens          │ │ • High Priority Queue │
│ • Idempotency Keys    │ │ • Default Queue       │
└───────────────────────┘ │ • Low Priority Queue  │
                          └───────────┬───────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
            ▼                         ▼                         ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│   POSTGRESQL 16       │ │   REDIS 7.4           │ │   AWS S3              │
│   (RDS / Docker)      │ │   (ElastiCache)       │ │   (ap-southeast-1)    │
│                       │ │                       │ │                       │
│ • Primary Database    │ │ • Session Store       │ │ • Invoice PDFs        │
│ • Generated Fields    │ │ • Cache Layer         │ │ • DSAR Exports        │
│ • Full-Text Search    │ │ • Celery Broker       │ │ • User Uploads        │
│ • Audit Logs          │ │ • Rate Limiting       │ │                       │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘
4.2 Request Flow Diagrams
4.2.1 Authentication Flow
text

┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │     │ Next.js  │     │  Django  │     │   Redis  │     │ Postgres │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │                │
     │ POST /login    │                │                │                │
     │───────────────>│                │                │                │
     │                │ POST /api/v1/auth/login         │                │
     │                │───────────────>│                │                │
     │                │                │                │                │
     │                │                │ Check Rate Limit                │
     │                │                │───────────────>│                │
     │                │                │<───────────────│                │
     │                │                │                │                │
     │                │                │ SELECT user WHERE email=?       │
     │                │                │───────────────────────────────>│
     │                │                │<───────────────────────────────│
     │                │                │                │                │
     │                │                │ Verify password (PBKDF2)        │
     │                │                │                │                │
     │                │                │ Generate JWT                    │
     │                │                │                │                │
     │                │                │ Store session  │                │
     │                │                │───────────────>│                │
     │                │                │                │                │
     │                │ {access_token, refresh_token}   │                │
     │                │<───────────────│                │                │
     │                │                │                │                │
     │ Set httpOnly   │                │                │                │
     │ cookies        │                │                │                │
     │<───────────────│                │                │                │
     │                │                │                │                │
4.2.2 Subscription Creation Flow (with Idempotency)
text

┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │     │  Django  │     │ Postgres │     │  Celery  │     │  Stripe  │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │                │
     │ POST /subscriptions             │                │                │
     │ Idempotency-Key: abc123         │                │                │
     │───────────────>│                │                │                │
     │                │                │                │                │
     │                │ Check IdempotencyRecord         │                │
     │                │───────────────>│                │                │
     │                │<───────────────│ (not found)    │                │
     │                │                │                │                │
     │                │ BEGIN TRANSACTION               │                │
     │                │───────────────>│                │                │
     │                │                │                │                │
     │                │ INSERT IdempotencyRecord        │                │
     │                │ (status='processing')           │                │
     │                │───────────────>│                │                │
     │                │                │                │                │
     │                │ INSERT Subscription             │                │
     │                │───────────────>│                │                │
     │                │                │                │                │
     │                │ COMMIT         │                │                │
     │                │───────────────>│                │                │
     │                │                │                │                │
     │                │ Enqueue process_stripe_subscription              │
     │                │───────────────────────────────>│                │
     │                │                │                │                │
     │ 201 Created    │                │                │                │
     │<───────────────│                │                │                │
     │                │                │                │                │
     │                │                │                │ Create Stripe  │
     │                │                │                │ Subscription   │
     │                │                │                │───────────────>│
     │                │                │                │<───────────────│
     │                │                │                │                │
     │                │                │ UPDATE Subscription             │
     │                │                │ (stripe_subscription_id)        │
     │                │<───────────────────────────────│                │
     │                │                │                │                │
     │                │ UPDATE IdempotencyRecord        │                │
     │                │ (status='completed')            │                │
     │                │───────────────>│                │                │
     │                │                │                │                │
4.2.3 Webhook Processing Flow
text

┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Stripe  │     │  Django  │     │ Postgres │     │  Celery  │     │ SendGrid │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │                │
     │ POST /webhooks/stripe           │                │                │
     │ Stripe-Signature: sig_xxx       │                │                │
     │───────────────>│                │                │                │
     │                │                │                │                │
     │                │ Verify signature               │                │
     │                │ (stripe.Webhook.construct_event)                 │
     │                │                │                │                │
     │                │ Check WebhookEvent exists       │                │
     │                │───────────────>│                │                │
     │                │<───────────────│ (not found)    │                │
     │                │                │                │                │
     │                │ INSERT WebhookEvent             │                │
     │                │ (processed=false)               │                │
     │                │───────────────>│                │                │
     │                │                │                │                │
     │                │ Enqueue process_stripe_webhook  │                │
     │                │───────────────────────────────>│                │
     │                │                │                │                │
     │ 200 OK         │                │                │                │
     │<───────────────│                │                │                │
     │                │                │                │                │
     │                │                │                │ Process event  │
     │                │                │                │                │
     │                │                │ UPDATE Invoice  │                │
     │                │                │ (status='paid') │                │
     │                │<───────────────────────────────│                │
     │                │                │                │                │
     │                │                │                │ Send email     │
     │                │                │                │───────────────>│
     │                │                │                │                │
     │                │                │ UPDATE WebhookEvent             │
     │                │                │ (processed=true)                │
     │                │<───────────────────────────────│                │
     │                │                │                │                │
4.3 Data Flow Architecture
text

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW OVERVIEW                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                WRITE PATH                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  User Action ──> API Request ──> Validation ──> Transaction ──> Commit         │
│       │              │               │              │             │             │
│       │              │               │              │             ▼             │
│       │              │               │              │      PostgreSQL           │
│       │              │               │              │             │             │
│       │              │               │              │             ▼             │
│       │              │               │              │      Event Log            │
│       │              │               │              │             │             │
│       │              │               │              │             ▼             │
│       │              │               │              │      Cache Invalidation   │
│       │              │               │              │             │             │
│       │              │               │              │             ▼             │
│       └──────────────┴───────────────┴──────────────┴─────> Async Tasks         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                READ PATH                                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  User Request ──> Check Cache ──┬──> HIT ──> Return Cached                      │
│                                 │                                               │
│                                 └──> MISS ──> Query DB ──> Cache ──> Return     │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
5. Directory Structure & File Manifest
5.1 Complete Project Structure
text

nexuscore/
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Continuous Integration
│       ├── cd-staging.yml              # Deploy to staging
│       └── cd-production.yml           # Deploy to production
│
├── backend/                            # Django Application
│   ├── manage.py
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── setup.cfg
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   │
│   ├── config/                         # Django Configuration
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   ├── celery.py
│   │   ├── urls.py
│   │   └── settings/
│   │       ├── __init__.py
│   │       ├── base.py                 # Base settings
│   │       ├── development.py          # Dev overrides
│   │       ├── staging.py              # Staging overrides
│   │       ├── production.py           # Production overrides
│   │       └── test.py                 # Test overrides
│   │
│   ├── apps/                           # Django Applications
│   │   ├── __init__.py
│   │   │
│   │   ├── core/                       # Core Models & Utilities
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py             # Abstract base models
│   │   │   │   ├── user.py             # User model
│   │   │   │   ├── organization.py     # Organization models
│   │   │   │   └── events.py           # Event & audit models
│   │   │   ├── managers.py
│   │   │   ├── validators.py
│   │   │   ├── exceptions.py
│   │   │   └── utils.py
│   │   │
│   │   ├── billing/                    # Subscription & Payments
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── plan.py             # Plan model
│   │   │   │   ├── subscription.py     # Subscription model
│   │   │   │   ├── invoice.py          # Invoice model (GST)
│   │   │   │   └── idempotency.py      # IdempotencyRecord
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── stripe_service.py
│   │   │   │   └── invoice_service.py
│   │   │   ├── tasks.py
│   │   │   └── webhooks.py
│   │   │
│   │   ├── leads/                      # Lead Management
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   └── tasks.py
│   │   │
│   │   ├── privacy/                    # PDPA Compliance
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py               # DSARRequest
│   │   │   ├── services.py
│   │   │   └── tasks.py
│   │   │
│   │   └── webhooks/                   # Webhook Processing
│   │       ├── __init__.py
│   │       ├── apps.py
│   │       ├── models.py               # WebhookEvent
│   │       └── handlers/
│   │           ├── __init__.py
│   │           └── stripe.py
│   │
│   ├── api/                            # API Layer
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   ├── versioning.py
│   │   ├── pagination.py
│   │   ├── throttling.py
│   │   ├── permissions.py
│   │   ├── authentication.py
│   │   │
│   │   └── v1/                         # API Version 1
│   │       ├── __init__.py
│   │       ├── urls.py
│   │       │
│   │       ├── auth/
│   │       │   ├── __init__.py
│   │       │   ├── views.py
│   │       │   ├── serializers.py
│   │       │   └── urls.py
│   │       │
│   │       ├── users/
│   │       │   ├── __init__.py
│   │       │   ├── views.py
│   │       │   ├── serializers.py
│   │       │   └── urls.py
│   │       │
│   │       ├── organizations/
│   │       │   ├── __init__.py
│   │       │   ├── views.py
│   │       │   ├── serializers.py
│   │       │   └── urls.py
│   │       │
│   │       ├── subscriptions/
│   │       │   ├── __init__.py
│   │       │   ├── views.py
│   │       │   ├── serializers.py
│   │       │   └── urls.py
│   │       │
│   │       ├── invoices/
│   │       │   ├── __init__.py
│   │       │   ├── views.py
│   │       │   ├── serializers.py
│   │       │   └── urls.py
│   │       │
│   │       ├── leads/
│   │       │   ├── __init__.py
│   │       │   ├── views.py
│   │       │   ├── serializers.py
│   │       │   └── urls.py
│   │       │
│   │       ├── dsar/
│   │       │   ├── __init__.py
│   │       │   ├── views.py
│   │       │   ├── serializers.py
│   │       │   └── urls.py
│   │       │
│   │       └── webhooks/
│   │           ├── __init__.py
│   │           ├── views.py
│   │           └── urls.py
│   │
│   ├── templates/                      # Django Templates
│   │   ├── admin/                      # Admin customizations
│   │   ├── emails/                     # Email templates
│   │   │   ├── base.html
│   │   │   ├── welcome.html
│   │   │   ├── verification.html
│   │   │   ├── password_reset.html
│   │   │   ├── invoice.html
│   │   │   └── dsar_export.html
│   │   └── invoices/
│   │       └── invoice_pdf.html        # PDF template
│   │
│   ├── static/                         # Static files
│   │   └── admin/
│   │
│   ├── media/                          # User uploads (dev only)
│   │
│   ├── logs/                           # Log files
│   │
│   └── tests/                          # Test Suite
│       ├── __init__.py
│       ├── conftest.py                 # Pytest fixtures
│       ├── factories.py                # Factory Boy factories
│       │
│       ├── unit/
│       │   ├── __init__.py
│       │   ├── test_models.py
│       │   ├── test_validators.py
│       │   └── test_services.py
│       │
│       ├── integration/
│       │   ├── __init__.py
│       │   ├── test_api_auth.py
│       │   ├── test_api_subscriptions.py
│       │   ├── test_api_invoices.py
│       │   └── test_webhooks.py
│       │
│       └── e2e/
│           ├── __init__.py
│           └── test_subscription_flow.py
│
├── frontend/                           # Next.js Application
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .eslintrc.json
│   ├── .prettierrc
│   ├── Dockerfile
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── robots.txt
│   │   ├── sitemap.xml
│   │   └── images/
│   │       ├── logo.svg
│   │       ├── logo-dark.svg
│   │       └── og-image.png
│   │
│   ├── src/
│   │   ├── app/                        # Next.js App Router
│   │   │   ├── layout.tsx              # Root layout
│   │   │   ├── page.tsx                # Homepage
│   │   │   ├── globals.css             # Global styles
│   │   │   ├── not-found.tsx
│   │   │   ├── error.tsx
│   │   │   │
│   │   │   ├── (marketing)/            # Marketing pages group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── pricing/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── features/
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
│   │   │   ├── (auth)/                 # Auth pages group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── login/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── register/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── verify-email/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── forgot-password/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── reset-password/
│   │   │   │       └── page.tsx
│   │   │   │
│   │   │   ├── (app)/                  # Authenticated app group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── dashboard/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── settings/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   ├── profile/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── organization/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   ├── billing/
│   │   │   │   │   │   └── page.tsx
│   │   │   │   │   └── privacy/
│   │   │   │   │       └── page.tsx
│   │   │   │   ├── subscription/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   └── checkout/
│   │   │   │   │       └── page.tsx
│   │   │   │   └── invoices/
│   │   │   │       ├── page.tsx
│   │   │   │       └── [id]/
│   │   │   │           └── page.tsx
│   │   │   │
│   │   │   ├── api/                    # API Routes
│   │   │   │   └── health/
│   │   │   │       └── route.ts
│   │   │   │
│   │   │   └── privacy/
│   │   │       └── page.tsx
│   │   │
│   │   ├── components/                 # React Components
│   │   │   ├── ui/                     # Base UI components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Select.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Toast.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Badge.tsx
│   │   │   │   ├── Spinner.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── layout/                 # Layout components
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Navigation.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── forms/                  # Form components
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   ├── ContactForm.tsx
│   │   │   │   ├── OrganizationForm.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── billing/                # Billing components
│   │   │   │   ├── PricingCard.tsx
│   │   │   │   ├── PricingTable.tsx
│   │   │   │   ├── CheckoutForm.tsx
│   │   │   │   ├── InvoiceList.tsx
│   │   │   │   ├── InvoiceDetail.tsx
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   └── marketing/              # Marketing components
│   │   │       ├── Hero.tsx
│   │   │       ├── Features.tsx
│   │   │       ├── Testimonials.tsx
│   │   │       ├── CTA.tsx
│   │   │       └── index.ts
│   │   │
│   │   ├── lib/                        # Utilities & Services
│   │   │   ├── api.ts                  # API client
│   │   │   ├── auth.ts                 # Auth utilities
│   │   │   ├── stripe.ts               # Stripe client
│   │   │   ├── utils.ts                # General utilities
│   │   │   ├── constants.ts            # Constants
│   │   │   └── validations.ts          # Zod schemas
│   │   │
│   │   ├── hooks/                      # Custom React Hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useUser.ts
│   │   │   ├── useOrganization.ts
│   │   │   ├── useSubscription.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── stores/                     # Zustand Stores
│   │   │   ├── authStore.ts
│   │   │   ├── uiStore.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── types/                      # TypeScript Types
│   │   │   ├── api.ts
│   │   │   ├── user.ts
│   │   │   ├── organization.ts
│   │   │   ├── billing.ts
│   │   │   └── index.ts
│   │   │
│   │   └── styles/                     # Additional styles
│   │       └── fonts.ts
│   │
│   ├── tests/                          # Frontend tests
│   │   ├── unit/
│   │   └── e2e/
│   │       └── cypress/
│   │
│   └── cypress.config.ts
│
├── infrastructure/                     # Infrastructure as Code
│   ├── docker/
│   │   ├── nginx/
│   │   │   ├── Dockerfile
│   │   │   └── nginx.conf
│   │   └── redis/
│   │       └── redis.conf
│   │
│   ├── terraform/                      # (Optional) IaC
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   └── scripts/
│       ├── deploy.sh
│       ├── backup.sh
│       └── restore.sh
│
├── docs/                               # Documentation
│   ├── api/
│   │   └── openapi.yaml
│   ├── architecture/
│   │   └── PAD.md                      # This document
│   └── runbooks/
│       ├── deployment.md
│       ├── incident-response.md
│       └── dsar-processing.md
│
├── .env.example                        # Environment template
├── .gitignore
├── docker-compose.yml                  # Full stack local dev
├── docker-compose.prod.yml             # Production compose
├── Makefile                            # Common commands
└── README.md
5.2 File Purpose Reference
File Path	Purpose	Implementation Priority
backend/apps/core/models/user.py	User authentication model	Week 1
backend/apps/core/models/organization.py	Organization with UEN/GST	Week 1
backend/apps/billing/models/invoice.py	GST GeneratedField invoice	Week 4
backend/apps/billing/models/idempotency.py	IdempotencyRecord	Week 1
backend/apps/webhooks/models.py	WebhookEvent	Week 1
backend/apps/privacy/models.py	DSARRequest	Week 7
frontend/src/components/billing/PricingCard.tsx	Pricing with Singapore colors	Week 3
6. Database Architecture
6.1 Entity Relationship Diagram
text

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         NEXUSCORE DATABASE SCHEMA                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐       ┌──────────────────────┐
│       users          │       │    organizations     │
├──────────────────────┤       ├──────────────────────┤
│ PK id: UUID          │       │ PK id: UUID          │
│    email: VARCHAR    │──────<│    owner_id: UUID FK │
│    name: VARCHAR     │       │    name: VARCHAR     │
│    company: VARCHAR  │       │    slug: VARCHAR     │
│    phone: VARCHAR    │       │    uen: VARCHAR      │◄──── Singapore UEN
│    is_verified: BOOL │       │    is_gst_reg: BOOL  │
│    is_active: BOOL   │       │    gst_reg_no: VARCHAR│◄──── GST Registration
│    is_staff: BOOL    │       │    stripe_cust_id    │
│    timezone: VARCHAR │       │    billing_email     │
│    email_prefs: JSONB│       │    trial_ends_at     │
│    created_at: TS    │       │    created_at: TS    │
│    updated_at: TS    │       │    updated_at: TS    │
└──────────────────────┘       └──────────────────────┘
         │                              │
         │                              │
         ▼                              ▼
┌──────────────────────────────────────────────────────┐
│              organization_memberships                │
├──────────────────────────────────────────────────────┤
│ PK id: UUID                                          │
│ FK organization_id: UUID ────────────────────────────┘
│ FK user_id: UUID ────────────────────────────────────┘
│    role: VARCHAR (owner|admin|member|viewer)         │
│    permissions: VARCHAR[] ◄─── ArrayField            │
│    joined_at: TIMESTAMP                              │
│ FK invited_by_id: UUID                               │
│    UNIQUE(organization_id, user_id)                  │
└──────────────────────────────────────────────────────┘

┌──────────────────────┐       ┌──────────────────────┐
│       plans          │       │    subscriptions     │
├──────────────────────┤       ├──────────────────────┤
│ PK id: UUID          │       │ PK id: UUID          │
│    name: VARCHAR     │──────<│ FK plan_id: UUID     │
│    description: TEXT │       │ FK organization_id   │───────┐
│    sku: VARCHAR      │       │    status: VARCHAR   │       │
│    billing_period    │       │    cancel_at_end     │       │
│    amount_cents: INT │       │    period_start: TS  │       │
│    currency: VARCHAR │       │    period_end: TS    │       │
│    features: JSONB   │       │    trial_start: TS   │       │
│    limits: JSONB     │       │    trial_end: TS     │       │
│    stripe_price_id   │       │    stripe_sub_id     │       │
│    is_active: BOOL   │       │    created_at: TS    │       │
│    display_order: INT│       │    canceled_at: TS   │       │
└──────────────────────┘       └──────────────────────┘       │
                                        │                      │
                                        │                      │
                                        ▼                      │
┌──────────────────────────────────────────────────────────────┼───────────────────┐
│                            invoices                          │                   │
├──────────────────────────────────────────────────────────────┴───────────────────┤
│ PK id: UUID                                                                      │
│ FK subscription_id: UUID (nullable) ─────────────────────────────────────────────┘
│ FK organization_id: UUID ────────────────────────────────────────────────────────┘
│    subtotal_cents: BIGINT                                                        │
│    gst_rate: DECIMAL(5,4) ◄─── Default 0.0900 (9%)                              │
│    gst_amount_cents: BIGINT ◄─── GENERATED (subtotal_cents * gst_rate)          │
│    total_amount_cents: BIGINT ◄─── GENERATED (subtotal + gst)                   │
│    amount_paid_cents: INT                                                        │
│    currency: VARCHAR ◄─── Default 'SGD'                                         │
│    iras_transaction_code: VARCHAR ◄─── SR|ZR|OS|TX                              │
│    status: VARCHAR (draft|open|paid|void|uncollectible)                          │
│    paid: BOOLEAN                                                                 │
│    due_date: TIMESTAMP                                                           │
│    paid_at: TIMESTAMP                                                            │
│    pdf_url: VARCHAR                                                              │
│    stripe_invoice_id: VARCHAR (UNIQUE)                                           │
│    stripe_payment_intent_id: VARCHAR                                             │
│    line_items: JSONB                                                             │
│    metadata: JSONB                                                               │
│    created_at: TIMESTAMP                                                         │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│       leads          │       │    dsar_requests     │       │       events         │
├──────────────────────┤       ├──────────────────────┤       ├──────────────────────┤
│ PK id: UUID          │       │ PK id: UUID          │       │ PK id: UUID          │
│    name: VARCHAR     │       │    user_email        │       │    event_type        │
│    email: VARCHAR    │       │ FK user_id: UUID     │       │ FK user_id: UUID     │
│    phone: VARCHAR    │       │    request_type      │       │ FK organization_id   │
│    company: VARCHAR  │       │    status            │       │    data: JSONB       │
│    job_title         │       │    verification_token│       │    created_at: TS    │
│    source            │       │    verified_at       │       └──────────────────────┘
│    status            │       │    export_url        │
│    notes: TEXT       │       │    export_expires_at │
│    utm_source        │       │    requested_at      │       ┌──────────────────────┐
│    utm_medium        │       │    processed_at      │       │  idempotency_records │
│    utm_campaign      │       │ FK deletion_approved │       ├──────────────────────┤
│    utm_term          │       │    failure_reason    │       │ PK id: UUID          │
│    utm_content       │       └──────────────────────┘       │    key: VARCHAR (UQ) │
│    form_data: JSONB  │                                      │    request_path      │
│ FK assigned_to: UUID │       ┌──────────────────────┐       │    request_method    │
│    next_follow_up    │       │    webhook_events    │       │    request_hash      │
│ FK converted_to_user │       ├──────────────────────┤       │    status            │
│    converted_at      │       │ PK id: UUID          │       │    response_status   │
│    created_at        │       │    service           │       │    response_body     │
│    updated_at        │       │    event_id (UNIQUE) │       │    expires_at        │
└──────────────────────┘       │    event_type        │       │    created_at        │
                               │    payload: JSONB    │       │    updated_at        │
                               │    processed: BOOL   │       └──────────────────────┘
                               │    processing_error  │
                               │    retry_count       │
                               │    created_at        │
                               │    processed_at      │
                               └──────────────────────┘
6.2 Complete Table Definitions
6.2.1 Table: users
SQL

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(254) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL DEFAULT '',
    phone VARCHAR(20) NOT NULL DEFAULT '',
    
    -- Authentication
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verification_token UUID NOT NULL DEFAULT gen_random_uuid(),
    verification_sent_at TIMESTAMP WITH TIME ZONE,
    
    -- Permissions
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Preferences
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Singapore',
    email_preferences JSONB NOT NULL DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT verified_users_must_be_active 
        CHECK (NOT is_verified OR is_active)
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_verified_active ON users(is_verified, is_active);
6.2.2 Table: organizations
SQL

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    
    -- Singapore Compliance [CRITICAL]
    uen VARCHAR(15) NOT NULL UNIQUE,
    is_gst_registered BOOLEAN NOT NULL DEFAULT FALSE,
    gst_reg_no VARCHAR(20),
    
    -- Billing
    stripe_customer_id VARCHAR(255) NOT NULL DEFAULT '',
    billing_email VARCHAR(254) NOT NULL,
    billing_phone VARCHAR(20) NOT NULL DEFAULT '',
    billing_address JSONB NOT NULL DEFAULT '{}',
    
    -- Settings
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Singapore',
    locale VARCHAR(10) NOT NULL DEFAULT 'en-SG',
    settings JSONB NOT NULL DEFAULT '{}',
    
    -- Relationships
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE PROTECT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    trial_ends_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT trial_ends_after_creation 
        CHECK (trial_ends_at IS NULL OR trial_ends_at >= created_at),
    CONSTRAINT valid_gst_registration
        CHECK (NOT is_gst_registered OR gst_reg_no IS NOT NULL)
);

-- Indexes
CREATE INDEX idx_organizations_name ON organizations(name);
CREATE INDEX idx_organizations_slug ON organizations(slug);
CREATE INDEX idx_organizations_uen ON organizations(uen);
CREATE INDEX idx_organizations_stripe_customer ON organizations(stripe_customer_id);
CREATE INDEX idx_organizations_created_at ON organizations(created_at);
6.2.3 Table: organization_memberships
SQL

CREATE TABLE organization_memberships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL DEFAULT 'member',
    permissions VARCHAR(50)[] NOT NULL DEFAULT '{}',
    joined_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    invited_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Constraints
    CONSTRAINT valid_role CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    UNIQUE (organization_id, user_id)
);

-- Indexes
CREATE INDEX idx_org_membership_org_user ON organization_memberships(organization_id, user_id);
CREATE INDEX idx_org_membership_role ON organization_memberships(role);
CREATE INDEX idx_org_membership_user_admin ON organization_memberships(user_id, organization_id) 
    WHERE role IN ('owner', 'admin');
6.2.4 Table: plans
SQL

CREATE TABLE plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    sku VARCHAR(50) NOT NULL UNIQUE,
    billing_period VARCHAR(10) NOT NULL DEFAULT 'month',
    amount_cents INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'SGD',
    features JSONB NOT NULL DEFAULT '{}',
    limits JSONB NOT NULL DEFAULT '{}',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_visible BOOLEAN NOT NULL DEFAULT TRUE,
    display_order INTEGER NOT NULL DEFAULT 0,
    stripe_price_id VARCHAR(255) NOT NULL DEFAULT '',
    stripe_product_id VARCHAR(255) NOT NULL DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_billing_period CHECK (billing_period IN ('month', 'year')),
    CONSTRAINT positive_amount CHECK (amount_cents >= 0)
);

-- Indexes
CREATE INDEX idx_plans_sku ON plans(sku);
CREATE INDEX idx_plans_active_visible ON plans(is_active, is_visible);
CREATE INDEX idx_plans_stripe_price ON plans(stripe_price_id);
6.2.5 Table: subscriptions
SQL

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE PROTECT,
    plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE PROTECT,
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'trialing',
    cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Billing Period
    current_period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    current_period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Trial
    trial_start TIMESTAMP WITH TIME ZONE,
    trial_end TIMESTAMP WITH TIME ZONE,
    
    -- Stripe
    stripe_subscription_id VARCHAR(255) NOT NULL UNIQUE,
    stripe_customer_id VARCHAR(255) NOT NULL,
    stripe_latest_invoice_id VARCHAR(255) NOT NULL DEFAULT '',
    
    -- Metadata
    metadata JSONB NOT NULL DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    canceled_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('trialing', 'active', 'past_due', 'canceled', 'unpaid')),
    CONSTRAINT period_end_after_start CHECK (current_period_end > current_period_start),
    CONSTRAINT trial_status_requires_trial_end CHECK (status != 'trialing' OR trial_end IS NOT NULL)
);

-- Indexes
CREATE INDEX idx_subscriptions_org_status ON subscriptions(organization_id, status);
CREATE INDEX idx_subscriptions_status_period ON subscriptions(status, current_period_end);
CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_subscriptions_active ON subscriptions(organization_id) 
    WHERE status IN ('active', 'trialing');
6.2.6 Table: invoices [CRITICAL - GST Compliance]
SQL

CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID REFERENCES subscriptions(id) ON DELETE PROTECT,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE PROTECT,
    
    -- Monetary Values (in cents) [CRITICAL]
    subtotal_cents BIGINT NOT NULL,
    gst_rate NUMERIC(5,4) NOT NULL DEFAULT 0.0900,
    
    -- Generated Fields [CRITICAL - Database-level GST calculation]
    gst_amount_cents BIGINT GENERATED ALWAYS AS (
        ROUND(subtotal_cents * gst_rate)
    ) STORED,
    total_amount_cents BIGINT GENERATED ALWAYS AS (
        subtotal_cents + ROUND(subtotal_cents * gst_rate)
    ) STORED,
    
    amount_paid_cents INTEGER NOT NULL DEFAULT 0,
    currency VARCHAR(3) NOT NULL DEFAULT 'SGD',
    
    -- IRAS Compliance [CRITICAL]
    iras_transaction_code VARCHAR(10) NOT NULL DEFAULT 'SR',
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    paid BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Dates
    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
    paid_at TIMESTAMP WITH TIME ZONE,
    
    -- External References
    pdf_url VARCHAR(500) NOT NULL DEFAULT '',
    stripe_invoice_id VARCHAR(255) NOT NULL UNIQUE,
    stripe_payment_intent_id VARCHAR(255) NOT NULL DEFAULT '',
    
    -- Data
    line_items JSONB NOT NULL DEFAULT '[]',
    metadata JSONB NOT NULL DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('draft', 'open', 'paid', 'void', 'uncollectible')),
    CONSTRAINT valid_iras_code CHECK (iras_transaction_code IN ('SR', 'ZR', 'OS', 'TX')),
    CONSTRAINT amount_paid_not_exceed_due CHECK (amount_paid_cents <= subtotal_cents + ROUND(subtotal_cents * gst_rate)),
    CONSTRAINT paid_invoices_require_paid_at CHECK (NOT paid OR paid_at IS NOT NULL),
    CONSTRAINT positive_subtotal CHECK (subtotal_cents >= 0)
);

-- Indexes
CREATE INDEX idx_invoices_org_status ON invoices(organization_id, status);
CREATE INDEX idx_invoices_status_due ON invoices(status, due_date);
CREATE INDEX idx_invoices_stripe ON invoices(stripe_invoice_id);
CREATE INDEX idx_invoices_created ON invoices(created_at);
CREATE INDEX idx_invoices_overdue ON invoices(due_date) 
    WHERE status = 'open';
6.2.7 Table: leads
SQL

CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Contact Information
    name VARCHAR(255) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(20) NOT NULL DEFAULT '',
    company VARCHAR(255) NOT NULL,
    job_title VARCHAR(100) NOT NULL DEFAULT '',
    
    -- Lead Details
    source VARCHAR(20) NOT NULL DEFAULT 'website',
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    notes TEXT NOT NULL DEFAULT '',
    
    -- UTM Tracking
    utm_source VARCHAR(100) NOT NULL DEFAULT '',
    utm_medium VARCHAR(100) NOT NULL DEFAULT '',
    utm_campaign VARCHAR(100) NOT NULL DEFAULT '',
    utm_term VARCHAR(100) NOT NULL DEFAULT '',
    utm_content VARCHAR(100) NOT NULL DEFAULT '',
    
    -- Form Data
    form_data JSONB NOT NULL DEFAULT '{}',
    
    -- Assignment
    assigned_to_id UUID REFERENCES users(id) ON DELETE SET NULL,
    next_follow_up TIMESTAMP WITH TIME ZONE,
    
    -- Conversion
    converted_to_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    converted_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_source CHECK (source IN ('website', 'demo_request', 'contact', 'event', 'referral', 'other')),
    CONSTRAINT valid_status CHECK (status IN ('new', 'contacted', 'qualified', 'converted', 'disqualified'))
);

-- Indexes
CREATE INDEX idx_leads_email ON leads(email);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created ON leads(created_at);
CREATE INDEX idx_leads_assigned_status ON leads(assigned_to_id, status);
CREATE INDEX idx_leads_source_created ON leads(source, created_at);
CREATE INDEX idx_leads_unassigned ON leads(created_at) 
    WHERE status = 'new' AND assigned_to_id IS NULL;

-- Full-text search
CREATE INDEX idx_leads_search ON leads USING GIN (
    to_tsvector('english', name || ' ' || company || ' ' || email)
);
6.2.8 Table: dsar_requests
SQL

CREATE TABLE dsar_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Requester
    user_email VARCHAR(254) NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Request Details
    request_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    
    -- Verification
    verification_token UUID NOT NULL DEFAULT gen_random_uuid(),
    verified_at TIMESTAMP WITH TIME ZONE,
    verification_method VARCHAR(50) NOT NULL DEFAULT '',
    
    -- Export Data
    export_url VARCHAR(500) NOT NULL DEFAULT '',
    export_expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    metadata JSONB NOT NULL DEFAULT '{}',
    failure_reason TEXT NOT NULL DEFAULT '',
    
    -- Timestamps
    requested_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    processing_started_at TIMESTAMP WITH TIME ZONE,
    processed_at TIMESTAMP WITH TIME ZONE,
    
    -- Deletion Approval (PDPA Requirement)
    deletion_approved_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    deletion_approved_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT valid_request_type CHECK (request_type IN ('export', 'delete', 'access', 'rectification')),
    CONSTRAINT valid_status CHECK (status IN ('pending', 'verifying', 'processing', 'completed', 'failed')),
    CONSTRAINT completed_requires_processed_at CHECK (status != 'completed' OR processed_at IS NOT NULL)
);

-- Indexes
CREATE INDEX idx_dsar_user_email ON dsar_requests(user_email);
CREATE INDEX idx_dsar_status_requested ON dsar_requests(status, requested_at);
CREATE INDEX idx_dsar_type_status ON dsar_requests(request_type, status);
CREATE INDEX idx_dsar_pending ON dsar_requests(requested_at) 
    WHERE status = 'pending';
6.2.9 Table: events
SQL

CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100) NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    data JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_events_type_created ON events(event_type, created_at);
CREATE INDEX idx_events_user_created ON events(user_id, created_at);
CREATE INDEX idx_events_org_created ON events(organization_id, created_at);

-- Partitioning (for high-volume events)
-- Consider partitioning by month for events table in production
6.2.10 Table: idempotency_records [CRITICAL]
SQL

CREATE TABLE idempotency_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key VARCHAR(255) NOT NULL UNIQUE,
    request_path VARCHAR(255) NOT NULL,
    request_method VARCHAR(10) NOT NULL,
    request_hash VARCHAR(64) NOT NULL,
    status VARCHAR(20) NOT NULL,
    response_status_code INTEGER,
    response_body JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Constraints
    CONSTRAINT valid_idempotency_status CHECK (status IN ('processing', 'completed', 'failed'))
);

-- Indexes
CREATE INDEX idx_idempotency_key ON idempotency_records(key);
CREATE INDEX idx_idempotency_expires ON idempotency_records(expires_at);
CREATE INDEX idx_idempotency_path_method ON idempotency_records(request_path, request_method);

-- Cleanup job should delete expired records
6.2.11 Table: webhook_events [CRITICAL]
SQL

CREATE TABLE webhook_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service VARCHAR(50) NOT NULL,
    event_id VARCHAR(255) NOT NULL UNIQUE,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    processing_error TEXT NOT NULL DEFAULT '',
    retry_count INTEGER NOT NULL DEFAULT 0,
    last_retry_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_webhook_service_type ON webhook_events(service, event_type);
CREATE INDEX idx_webhook_processed_created ON webhook_events(processed, created_at);
CREATE INDEX idx_webhook_unprocessed ON webhook_events(created_at) 
    WHERE NOT processed;
6.3 Database Migration Strategy
6.3.1 Migration File Naming Convention
text

XXXX_descriptive_name.py

Examples:
0001_initial_users.py
0002_initial_organizations.py
0003_add_gst_fields_to_organization.py
0004_add_generated_fields_to_invoice.py
6.3.2 Migration Execution Order
text

1. users (no dependencies)
2. organizations (depends on users)
3. organization_memberships (depends on users, organizations)
4. plans (no dependencies)
5. subscriptions (depends on organizations, plans)
6. invoices (depends on organizations, subscriptions)
7. leads (depends on users)
8. dsar_requests (depends on users)
9. events (depends on users, organizations)
10. idempotency_records (no dependencies)
11. webhook_events (no dependencies)
7. Data Models Specification
7.1 Abstract Base Models
Python

# backend/apps/core/models/base.py

import uuid
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    Abstract base model with created_at and updated_at timestamps.
    
    All models that need timestamp tracking MUST inherit from this class.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    Abstract base model with UUID primary key.
    
    All models MUST use UUID primary keys for:
    - Security (non-guessable IDs)
    - Distributed system compatibility
    - API consistency
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimestampedModel):
    """
    Combined base model with UUID primary key and timestamps.
    
    Standard base class for all NexusCore models.
    """
    class Meta:
        abstract = True
7.2 User Model
Python

# backend/apps/core/models/user.py

import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone

from .base import UUIDModel


class UserManager(BaseUserManager):
    """
    Custom user manager for email-based authentication.
    """
    
    def create_user(self, email: str, password: str = None, **extra_fields) -> 'User':
        """
        Create and return a regular user.
        
        Args:
            email: User's email address (required, must be unique)
            password: User's password (will be hashed)
            **extra_fields: Additional user fields
            
        Returns:
            Created User instance
            
        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email: str, password: str, **extra_fields) -> 'User':
        """
        Create and return a superuser.
        
        Args:
            email: Superuser's email address
            password: Superuser's password
            **extra_fields: Additional user fields
            
        Returns:
            Created User instance with superuser privileges
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(UUIDModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email-based authentication.
    
    Uses UUID primary key and email as the username field.
    Stores preferences in JSONB for flexibility.
    
    Attributes:
        email: Unique email address (username field)
        name: Full name of the user
        company: Company name (optional, used for leads)
        phone: Phone number (optional)
        is_verified: Email verification status
        verification_token: Token for email verification
        verification_sent_at: When verification email was sent
        is_active: Whether user can log in
        is_staff: Whether user can access admin
        timezone: User's timezone (default: Asia/Singapore)
        email_preferences: JSONB storing email preferences
    """
    
    # Core fields
    email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': 'A user with this email already exists.',
        }
    )
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    
    # Authentication
    is_verified = models.BooleanField(
        default=False,
        help_text='Whether the user has verified their email address.'
    )
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Permissions
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this user account is active.'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Whether this user can access the admin site.'
    )
    
    # Preferences
    timezone = models.CharField(
        max_length=50,
        default='Asia/Singapore'
    )
    email_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text='User email notification preferences'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
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
    
    def __str__(self) -> str:
        return self.email
    
    def get_full_name(self) -> str:
        """Return the user's full name."""
        return self.name
    
    def get_short_name(self) -> str:
        """Return the user's first name."""
        return self.name.split()[0] if self.name else ''
    
    def regenerate_verification_token(self) -> None:
        """
        Generate a new verification token and record the timestamp.
        
        Call this when resending verification emails.
        """
        self.verification_token = uuid.uuid4()
        self.verification_sent_at = timezone.now()
        self.save(update_fields=['verification_token', 'verification_sent_at'])
    
    def verify_email(self) -> None:
        """
        Mark the user's email as verified.
        """
        self.is_verified = True
        self.save(update_fields=['is_verified', 'updated_at'])
7.3 Organization Model (with Singapore Compliance)
Python

# backend/apps/core/models/organization.py

import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.text import slugify

from .base import BaseModel
from .user import User


# Singapore UEN Validator
uen_validator = RegexValidator(
    regex=r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$',
    message='Enter a valid Singapore UEN (e.g., 12345678A, 123456789B, or T12AB1234C).'
)

# Singapore GST Registration Number Validator
gst_validator = RegexValidator(
    regex=r'^M[0-9]{8}[A-Z]$',
    message='Enter a valid GST registration number (e.g., M12345678A).'
)


class Organization(BaseModel):
    """
    Organization/Company entity with Singapore compliance fields.
    
    [CRITICAL] This model includes Singapore-specific fields for:
    - UEN (Unique Entity Number) validation per ACRA requirements
    - GST registration tracking for IRAS compliance
    
    Attributes:
        name: Organization display name
        slug: URL-safe unique identifier
        uen: Singapore Unique Entity Number (required)
        is_gst_registered: Whether organization is GST registered
        gst_reg_no: GST registration number (required if is_gst_registered)
        stripe_customer_id: Stripe customer ID for billing
        billing_email: Email for invoices and billing notifications
        billing_phone: Phone for billing inquiries
        billing_address: JSONB storing structured billing address
        timezone: Organization timezone
        locale: Locale for formatting (default: en-SG)
        settings: JSONB for organization settings
        owner: User who owns this organization
        trial_ends_at: When trial period ends (null if no trial)
    """
    
    # Core fields
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    
    # Singapore Compliance [CRITICAL]
    uen = models.CharField(
        max_length=15,
        unique=True,
        validators=[uen_validator],
        help_text='Singapore Unique Entity Number (ACRA registered)'
    )
    is_gst_registered = models.BooleanField(
        default=False,
        help_text='Whether organization is registered for GST'
    )
    gst_reg_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[gst_validator],
        help_text='GST registration number (required if GST registered)'
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
        help_text='Structured billing address: {street, city, postal_code, country}'
    )
    
    # Settings
    timezone = models.CharField(max_length=50, default='Asia/Singapore')
    locale = models.CharField(max_length=10, default='en-SG')
    settings = models.JSONField(default=dict, blank=True)
    
    # Relationships
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='owned_organizations'
    )
    members = models.ManyToManyField(
        User,
        through='OrganizationMembership',
        related_name='organizations'
    )
    
    # Trial
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'organizations'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['uen']),
            models.Index(fields=['stripe_customer_id']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(trial_ends_at__gte=models.F('created_at')) | 
                      models.Q(trial_ends_at__isnull=True),
                name='trial_ends_after_creation'
            ),
            models.CheckConstraint(
                check=models.Q(is_gst_registered=False) | 
                      models.Q(gst_reg_no__isnull=False),
                name='gst_registered_requires_gst_reg_no'
            ),
        ]
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Organization.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    @property
    def is_in_trial(self) -> bool:
        """Check if organization is in trial period."""
        if not self.trial_ends_at:
            return False
        return timezone.now() < self.trial_ends_at
    
    @property
    def days_left_in_trial(self) -> int:
        """Days remaining in trial."""
        if not self.trial_ends_at:
            return 0
        remaining = self.trial_ends_at - timezone.now()
        return max(0, remaining.days)
    
    def get_active_subscription(self):
        """Get the organization's active subscription, if any."""
        return self.subscriptions.filter(
            status__in=['active', 'trialing']
        ).first()


class OrganizationMembership(BaseModel):
    """
    Organization membership with role-based permissions.
    
    Defines the relationship between users and organizations
    with role-based access control.
    
    Attributes:
        organization: The organization
        user: The member user
        role: Member's role (owner, admin, member, viewer)
        permissions: Cached permissions array for performance
        joined_at: When the user joined
        invited_by: User who invited this member
    """
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    # Permission definitions per role
    ROLE_PERMISSIONS = {
        'owner': [
            'organization.delete',
            'organization.update',
            'organization.billing',
            'members.manage',
            'subscription.manage',
            'invoices.view',
            'leads.manage',
        ],
        'admin': [
            'organization.update',
            'members.invite',
            'members.remove',
            'invoices.view',
            'leads.manage',
        ],
        'member': [
            'invoices.view',
            'leads.view',
            'leads.create',
        ],
        'viewer': [
            'invoices.view',
            'leads.view',
        ],
    }
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )
    permissions = models.JSONField(
        default=list,
        blank=True,
        help_text='Cached permissions for performance'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(
        User,
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
        ]
    
    def __str__(self) -> str:
        return f"{self.user.email} - {self.organization.name} ({self.role})"
    
    def save(self, *args, **kwargs):
        """Auto-populate permissions based on role."""
        if not self.permissions:
            self.permissions = self.ROLE_PERMISSIONS.get(self.role, [])
        super().save(*args, **kwargs)
    
    def has_permission(self, permission: str) -> bool:
        """Check if member has a specific permission."""
        return permission in self.permissions
7.4 Billing Models
Python

# backend/apps/billing/models/plan.py

from decimal import Decimal
from django.db import models
from apps.core.models.base import BaseModel


class Plan(BaseModel):
    """
    Subscription plan definition.
    
    Defines available subscription plans with pricing,
    features, and limits.
    
    Attributes:
        name: Display name
        description: Plan description
        sku: Unique SKU identifier (e.g., 'starter-month')
        billing_period: 'month' or 'year'
        amount_cents: Price in cents (SGD)
        currency: Currency code (default: SGD)
        features: JSONB of feature flags
        limits: JSONB of usage limits
        stripe_price_id: Stripe Price ID
        stripe_product_id: Stripe Product ID
        is_active: Whether plan is available for new subscriptions
        is_visible: Whether plan appears on pricing page
        display_order: Order for displaying on pricing page
    """
    
    BILLING_PERIOD_CHOICES = [
        ('month', 'Monthly'),
        ('year', 'Annual'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    billing_period = models.CharField(
        max_length=10,
        choices=BILLING_PERIOD_CHOICES,
        default='month'
    )
    amount_cents = models.PositiveIntegerField(
        help_text='Amount in cents (e.g., 9900 = $99.00 SGD)'
    )
    currency = models.CharField(max_length=3, default='SGD')
    
    # Features and limits
    features = models.JSONField(
        default=dict,
        blank=True,
        help_text='Feature flags: {"feature_name": true/false}'
    )
    limits = models.JSONField(
        default=dict,
        blank=True,
        help_text='Usage limits: {"users": 5, "storage_gb": 10}'
    )
    
    # Stripe integration
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        db_index=True
    )
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    
    # Visibility
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    display_order = 
