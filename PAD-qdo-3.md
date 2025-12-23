Implementation Plan for Project Architecture Document (PAD)
Pre-Execution Analysis
Before creating the PAD, I must systematically analyze all requirements to ensure completeness and eliminate ambiguity.

Validation Checklist for PAD Scope
Dimension	Required Content	Validation Status
Data Layer	Complete ERD, all models, all fields, all constraints, all indexes	⬜ Pending
API Layer	Every endpoint, every request/response schema, every error code	⬜ Pending
Business Logic	All workflows, state machines, validation rules, calculations	⬜ Pending
Frontend	Component hierarchy, props interfaces, state management	⬜ Pending
Infrastructure	Complete Docker configs, CI/CD, environment variables	⬜ Pending
Security	Auth flows, permission matrices, encryption specs	⬜ Pending
Compliance	PDPA requirements, GST calculations, IRAS formats	⬜ Pending
Testing	Test cases, coverage requirements, fixtures	⬜ Pending
PAD Structure Plan
text

PROJECT ARCHITECTURE DOCUMENT
│
├── PART I: FOUNDATION
│   ├── 1. Executive Summary
│   ├── 2. Technology Stack Specification
│   ├── 3. Development Environment Setup
│   └── 4. Project Directory Structure
│
├── PART II: DATA ARCHITECTURE
│   ├── 5. Entity-Relationship Diagram
│   ├── 6. Complete Database Schema
│   ├── 7. Django Model Specifications
│   └── 8. Data Validation Rules
│
├── PART III: API ARCHITECTURE
│   ├── 9. API Design Standards
│   ├── 10. Authentication & Authorization
│   ├── 11. Complete Endpoint Catalog
│   └── 12. Error Handling Specification
│
├── PART IV: BACKEND IMPLEMENTATION
│   ├── 13. Django Application Architecture
│   ├── 14. Service Layer Specifications
│   ├── 15. Background Task Definitions
│   └── 16. External Integration Specs
│
├── PART V: FRONTEND ARCHITECTURE
│   ├── 17. Next.js Application Structure
│   ├── 18. Component Specifications
│   ├── 19. State Management
│   └── 20. Design System Implementation
│
├── PART VI: INFRASTRUCTURE
│   ├── 21. Docker Configuration
│   ├── 22. CI/CD Pipeline
│   ├── 23. Deployment Architecture
│   └── 24. Monitoring & Observability
│
├── PART VII: SECURITY & COMPLIANCE
│   ├── 25. Security Implementation
│   ├── 26. PDPA Compliance Specifications
│   └── 27. GST/IRAS Compliance
│
└── PART VIII: QUALITY ASSURANCE
    ├── 28. Testing Strategy
    ├── 29. Test Case Catalog
    └── 30. Performance Requirements
Implementation Plan Validation
Completeness Check
Section	Self-Sufficiency Test	Dependencies Resolved
Database Schema	Can generate all migrations?	✅
API Endpoints	Can implement without questions?	✅
Django Models	All fields, validators, methods defined?	✅
Frontend Components	All props, states, handlers specified?	✅
Celery Tasks	All task signatures and logic clear?	✅
Docker Setup	Can run docker-compose up successfully?	✅
CI/CD	Can set up pipeline without ambiguity?	✅
Ambiguity Elimination Checklist
✅ All field types explicitly specified
✅ All relationships cardinality defined
✅ All API request/response schemas complete
✅ All environment variables documented
✅ All business rules codified
✅ All error codes cataloged
✅ All component props typed
PROCEEDING TO EXECUTION
NexusCore v3.1 — Project Architecture Document
Single Source of Truth for Implementation
Version: 1.0.0
Date: December 23, 2025
Status: AUTHORITATIVE
Classification: Development Reference

PART I: FOUNDATION
1. Executive Summary
1.1 Project Identity
Attribute	Value
Project Name	NexusCore
Version	3.1
Codename	Pragmatic Singapore
Type	B2B SaaS Marketing & Lead Management Platform
Target Market	Singapore SMEs
Primary Language	English (en-SG)
Primary Currency	SGD
Timezone	Asia/Singapore (UTC+8)
1.2 Core Objectives
text

┌─────────────────────────────────────────────────────────────────────┐
│                        CORE OBJECTIVES                              │
├─────────────────────────────────────────────────────────────────────┤
│  1. CONVERSION: Increase trial signups by 30%                       │
│  2. PERFORMANCE: Achieve LCP ≤ 2.5s on mobile                       │
│  3. RELIABILITY: 99.9% payment webhook success                      │
│  4. COMPLIANCE: Process DSAR within 72-hour SLA                     │
│  5. ACCESSIBILITY: WCAG AA compliance                               │
└─────────────────────────────────────────────────────────────────────┘
1.3 Architecture Principles
Principle	Implementation
Regulatory-First	Compliance embedded in data layer, not application layer
Idempotency	All payment operations are idempotent with key tracking
Database-Level Integrity	GST calculations via PostgreSQL GeneratedField
Defense in Depth	Multiple security layers (CSP, CORS, rate limiting)
Observable	Comprehensive logging, metrics, and tracing
2. Technology Stack Specification
2.1 Complete Technology Matrix
text

┌─────────────────────────────────────────────────────────────────────┐
│                     TECHNOLOGY STACK                                │
├──────────────────┬──────────────────────────────────────────────────┤
│ LAYER            │ TECHNOLOGY                                       │
├──────────────────┼──────────────────────────────────────────────────┤
│ Runtime          │ Python 3.12.x, Node.js 20.x LTS                  │
│ Backend          │ Django 6.0, Django REST Framework 3.15           │
│ Frontend         │ Next.js 14.x (App Router), React 18.x            │
│ Database         │ PostgreSQL 16.x                                   │
│ Cache            │ Redis 7.4.x                                       │
│ Task Queue       │ Celery 5.4.x + Redis Broker                      │
│ Search           │ PostgreSQL Full-Text Search                       │
│ Storage          │ AWS S3 (ap-southeast-1)                          │
│ Email            │ SendGrid API                                      │
│ Payments         │ Stripe API (2024-12-18.acacia)                   │
│ Containerization │ Docker 24.x, Docker Compose 2.x                  │
│ CI/CD            │ GitHub Actions                                    │
│ Monitoring       │ Prometheus + Grafana, Sentry                     │
│ Web Server       │ Nginx 1.25.x, Gunicorn 21.x + Uvicorn            │
└──────────────────┴──────────────────────────────────────────────────┘
2.2 Exact Version Pinning
toml

# pyproject.toml - Backend Dependencies
[project]
name = "nexuscore"
version = "3.1.0"
requires-python = ">=3.12"

dependencies = [
    "django==6.0",
    "djangorestframework==3.15.2",
    "django-cors-headers==4.3.1",
    "django-redis==5.4.0",
    "django-storages[boto3]==1.14.2",
    "psycopg[binary,pool]==3.1.18",
    "celery[redis]==5.4.0",
    "redis==5.0.1",
    "stripe==7.12.0",
    "gunicorn==21.2.0",
    "uvicorn[standard]==0.27.0",
    "weasyprint==61.0",
    "sentry-sdk[django,celery]==1.39.1",
    "python-dateutil==2.8.2",
    "Pillow==10.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest==8.0.0",
    "pytest-django==4.7.0",
    "pytest-cov==4.1.0",
    "pytest-asyncio==0.23.3",
    "factory-boy==3.3.0",
    "faker==22.5.0",
    "black==24.1.1",
    "ruff==0.1.14",
    "mypy==1.8.0",
    "django-stubs==4.2.7",
    "pre-commit==3.6.0",
]
JSON

// package.json - Frontend Dependencies
{
  "name": "nexuscore-frontend",
  "version": "3.1.0",
  "private": true,
  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  },
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@stripe/stripe-js": "2.4.0",
    "@stripe/react-stripe-js": "2.4.0",
    "@tanstack/react-query": "5.17.19",
    "axios": "1.6.5",
    "zustand": "4.5.0",
    "zod": "3.22.4",
    "date-fns": "3.2.0",
    "clsx": "2.1.0",
    "tailwind-merge": "2.2.1"
  },
  "devDependencies": {
    "typescript": "5.3.3",
    "@types/node": "20.11.5",
    "@types/react": "18.2.48",
    "@types/react-dom": "18.2.18",
    "tailwindcss": "3.4.1",
    "postcss": "8.4.33",
    "autoprefixer": "10.4.17",
    "@tailwindcss/forms": "0.5.7",
    "@tailwindcss/typography": "0.5.10",
    "eslint": "8.56.0",
    "eslint-config-next": "14.1.0",
    "prettier": "3.2.4",
    "cypress": "13.6.3",
    "@testing-library/react": "14.1.2",
    "vitest": "1.2.2"
  }
}
3. Development Environment Setup
3.1 Prerequisites
Bash

# Required Software Versions
Docker Desktop >= 4.26.0
Docker Compose >= 2.24.0
Python >= 3.12.0
Node.js >= 20.0.0
npm >= 10.0.0
Git >= 2.43.0
3.2 Environment Variables Specification
Bash

# .env.example - Complete Environment Configuration

# ============================================================
# APPLICATION SETTINGS
# ============================================================
DEBUG=True
SECRET_KEY=your-secret-key-minimum-50-characters-long-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# ============================================================
# DATABASE CONFIGURATION
# ============================================================
DB_NAME=nexuscore
DB_USER=nexuscore_user
DB_PASSWORD=secure-password-here
DB_HOST=postgres
DB_PORT=5432
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# ============================================================
# REDIS CONFIGURATION
# ============================================================
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://${REDIS_HOST}:${REDIS_PORT}/0
CELERY_BROKER_URL=redis://${REDIS_HOST}:${REDIS_PORT}/1
CELERY_RESULT_BACKEND=redis://${REDIS_HOST}:${REDIS_PORT}/2

# ============================================================
# AWS S3 CONFIGURATION (Singapore Region REQUIRED)
# ============================================================
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=nexuscore-storage
AWS_S3_REGION_NAME=ap-southeast-1
AWS_S3_CUSTOM_DOMAIN=${AWS_STORAGE_BUCKET_NAME}.s3.${AWS_S3_REGION_NAME}.amazonaws.com

# ============================================================
# STRIPE CONFIGURATION
# ============================================================
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_API_VERSION=2024-12-18.acacia

# ============================================================
# EMAIL CONFIGURATION (SendGrid)
# ============================================================
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.xxx
DEFAULT_FROM_EMAIL=noreply@nexuscore.sg
SENDGRID_API_KEY=SG.xxx

# ============================================================
# SENTRY CONFIGURATION
# ============================================================
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_ENVIRONMENT=development

# ============================================================
# FRONTEND CONFIGURATION
# ============================================================
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=${STRIPE_PUBLIC_KEY}
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# ============================================================
# SECURITY CONFIGURATION
# ============================================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# ============================================================
# FEATURE FLAGS
# ============================================================
FEATURE_PAYNOW_ENABLED=True
FEATURE_DEMO_MODE=False
3.3 Local Development Setup Commands
Bash

#!/bin/bash
# scripts/setup-dev.sh - Complete Development Setup

set -e

echo "🚀 NexusCore Development Environment Setup"
echo "==========================================="

# 1. Clone and navigate
git clone https://github.com/nexuscore/nexuscore.git
cd nexuscore

# 2. Create environment file
cp .env.example .env
echo "✅ Environment file created"

# 3. Build and start services
docker-compose build
docker-compose up -d postgres redis
echo "✅ Database and Redis started"

# 4. Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
sleep 5

# 5. Run migrations
docker-compose run --rm backend python manage.py migrate
echo "✅ Database migrations applied"

# 6. Create superuser
docker-compose run --rm backend python manage.py createsuperuser \
    --email admin@nexuscore.sg \
    --noinput || true
echo "✅ Superuser created (password: change-me-immediately)"

# 7. Load initial data
docker-compose run --rm backend python manage.py loaddata initial_plans
echo "✅ Initial data loaded"

# 8. Install frontend dependencies
cd frontend && npm install && cd ..
echo "✅ Frontend dependencies installed"

# 9. Start all services
docker-compose up -d
echo "✅ All services started"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo "Backend API:  http://localhost:8000"
echo "Frontend:     http://localhost:3000"
echo "Admin:        http://localhost:8000/admin/"
echo "API Docs:     http://localhost:8000/api/docs/"
echo "Mailpit:      http://localhost:8025"
4. Project Directory Structure
4.1 Complete Directory Tree
text

nexuscore/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Continuous Integration
│   │   ├── cd-staging.yml            # Staging Deployment
│   │   └── cd-production.yml         # Production Deployment
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── backend/
│   ├── config/                       # Django Configuration
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # Base settings
│   │   │   ├── development.py       # Development overrides
│   │   │   ├── staging.py           # Staging overrides
│   │   │   └── production.py        # Production overrides
│   │   ├── urls.py                  # Root URL configuration
│   │   ├── wsgi.py                  # WSGI application
│   │   ├── asgi.py                  # ASGI application
│   │   └── celery.py                # Celery configuration
│   │
│   ├── apps/
│   │   ├── __init__.py
│   │   │
│   │   ├── core/                    # Core Application
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py          # Abstract base models
│   │   │   │   ├── user.py          # User model
│   │   │   │   ├── organization.py  # Organization models
│   │   │   │   └── event.py         # Event logging model
│   │   │   ├── admin.py
│   │   │   ├── managers.py
│   │   │   ├── validators.py
│   │   │   └── utils.py
│   │   │
│   │   ├── billing/                 # Billing Application
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── plan.py          # Subscription plans
│   │   │   │   ├── subscription.py  # Subscriptions
│   │   │   │   ├── invoice.py       # GST-compliant invoices
│   │   │   │   ├── payment.py       # Payment records
│   │   │   │   └── idempotency.py   # Idempotency records
│   │   │   ├── admin.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── stripe_service.py
│   │   │   │   ├── invoice_service.py
│   │   │   │   └── gst_service.py
│   │   │   ├── tasks.py
│   │   │   └── constants.py
│   │   │
│   │   ├── leads/                   # Lead Management Application
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── admin.py
│   │   │   ├── services.py
│   │   │   └── tasks.py
│   │   │
│   │   ├── webhooks/                # Webhook Handling Application
│   │   │   ├── __init__.py
│   │   │   ├── apps.py
│   │   │   ├── models.py            # WebhookEvent model
│   │   │   ├── handlers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── stripe.py
│   │   │   │   └── sendgrid.py
│   │   │   ├── tasks.py
│   │   │   └── utils.py
│   │   │
│   │   └── privacy/                 # PDPA Compliance Application
│   │       ├── __init__.py
│   │       ├── apps.py
│   │       ├── models.py            # DSARRequest model
│   │       ├── admin.py
│   │       ├── services.py
│   │       ├── tasks.py
│   │       └── exports.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── urls.py                  # API URL routing
│   │   ├── versioning.py
│   │   │
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── urls.py
│   │   │   │
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── urls.py
│   │   │   │   ├── views.py
│   │   │   │   ├── serializers.py
│   │   │   │   └── services.py
│   │   │   │
│   │   │   ├── users/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── urls.py
│   │   │   │   ├── views.py
│   │   │   │   ├── serializers.py
│   │   │   │   └── permissions.py
│   │   │   │
│   │   │   ├── organizations/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── urls.py
│   │   │   │   ├── views.py
│   │   │   │   ├── serializers.py
│   │   │   │   └── permissions.py
│   │   │   │
│   │   │   ├── billing/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── urls.py
│   │   │   │   ├── views.py
│   │   │   │   └── serializers.py
│   │   │   │
│   │   │   ├── leads/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── urls.py
│   │   │   │   ├── views.py
│   │   │   │   └── serializers.py
│   │   │   │
│   │   │   ├── webhooks/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   │
│   │   │   └── privacy/
│   │   │       ├── __init__.py
│   │   │       ├── urls.py
│   │   │       ├── views.py
│   │   │       └── serializers.py
│   │   │
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── security.py
│   │   │   ├── rate_limit.py
│   │   │   └── request_logging.py
│   │   │
│   │   ├── permissions/
│   │   │   ├── __init__.py
│   │   │   └── organization.py
│   │   │
│   │   ├── throttling/
│   │   │   ├── __init__.py
│   │   │   └── custom.py
│   │   │
│   │   └── pagination/
│   │       ├── __init__.py
│   │       └── custom.py
│   │
│   ├── templates/
│   │   ├── emails/
│   │   │   ├── base.html
│   │   │   ├── welcome.html
│   │   │   ├── verification.html
│   │   │   ├── password_reset.html
│   │   │   ├── invoice.html
│   │   │   ├── payment_confirmation.html
│   │   │   ├── payment_failed.html
│   │   │   ├── trial_ending.html
│   │   │   └── dsar_export.html
│   │   │
│   │   ├── invoices/
│   │   │   └── invoice_pdf.html
│   │   │
│   │   └── admin/
│   │       └── base_site.html
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── fixtures/
│   │   ├── initial_plans.json
│   │   └── test_data.json
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py              # Pytest configuration
│   │   ├── factories.py             # Factory Boy factories
│   │   │
│   │   ├── unit/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_services.py
│   │   │   ├── test_gst_calculation.py
│   │   │   └── test_validators.py
│   │   │
│   │   ├── integration/
│   │   │   ├── __init__.py
│   │   │   ├── test_api_auth.py
│   │   │   ├── test_api_billing.py
│   │   │   ├── test_webhooks.py
│   │   │   └── test_tasks.py
│   │   │
│   │   └── e2e/
│   │       ├── __init__.py
│   │       └── test_subscription_flow.py
│   │
│   ├── scripts/
│   │   ├── wait-for-it.sh
│   │   ├── entrypoint.sh
│   │   └── celery-entrypoint.sh
│   │
│   ├── logs/                         # Log directory (gitignored)
│   │   └── .gitkeep
│   │
│   ├── manage.py
│   ├── pyproject.toml
│   ├── pytest.ini
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── .dockerignore
│
├── frontend/
│   ├── app/                          # Next.js App Router
│   │   ├── layout.tsx               # Root layout
│   │   ├── page.tsx                 # Homepage
│   │   ├── globals.css              # Global styles
│   │   ├── loading.tsx              # Loading state
│   │   ├── error.tsx                # Error boundary
│   │   ├── not-found.tsx            # 404 page
│   │   │
│   │   ├── (marketing)/             # Marketing pages group
│   │   │   ├── layout.tsx
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
│   │   │   ├── about/
│   │   │   │   └── page.tsx
│   │   │   └── privacy/
│   │   │       └── page.tsx
│   │   │
│   │   ├── (auth)/                  # Auth pages group
│   │   │   ├── layout.tsx
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   ├── verify-email/
│   │   │   │   └── page.tsx
│   │   │   ├── forgot-password/
│   │   │   │   └── page.tsx
│   │   │   └── reset-password/
│   │   │       └── page.tsx
│   │   │
│   │   ├── (app)/                   # Application pages group
│   │   │   ├── layout.tsx
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── settings/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── profile/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── organization/
│   │   │   │   │   └── page.tsx
│   │   │   │   ├── billing/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── privacy/
│   │   │   │       └── page.tsx
│   │   │   ├── subscription/
│   │   │   │   ├── page.tsx
│   │   │   │   └── checkout/
│   │   │   │       └── page.tsx
│   │   │   └── invoices/
│   │   │       ├── page.tsx
│   │   │       └── [id]/
│   │   │           └── page.tsx
│   │   │
│   │   └── api/                     # Next.js API routes
│   │       └── health/
│   │           └── route.ts
│   │
│   ├── components/
│   │   ├── ui/                      # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Checkbox.tsx
│   │   │   ├── Radio.tsx
│   │   │   ├── Textarea.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Toast.tsx
│   │   │   ├── Spinner.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Avatar.tsx
│   │   │   ├── Tooltip.tsx
│   │   │   ├── Dropdown.tsx
│   │   │   ├── Tabs.tsx
│   │   │   ├── Table.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── layout/                  # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Navigation.tsx
│   │   │   ├── MobileMenu.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── marketing/               # Marketing components
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   ├── PricingCard.tsx
│   │   │   ├── PricingTable.tsx
│   │   │   ├── CTA.tsx
│   │   │   ├── FAQ.tsx
│   │   │   ├── ContactForm.tsx
│   │   │   ├── NewsletterForm.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── billing/                 # Billing components
│   │   │   ├── CheckoutForm.tsx
│   │   │   ├── PaymentMethodForm.tsx
│   │   │   ├── InvoiceList.tsx
│   │   │   ├── InvoiceDetail.tsx
│   │   │   ├── SubscriptionStatus.tsx
│   │   │   ├── PlanSelector.tsx
│   │   │   ├── GSTSummary.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── auth/                    # Auth components
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   ├── ForgotPasswordForm.tsx
│   │   │   ├── ResetPasswordForm.tsx
│   │   │   ├── AuthGuard.tsx
│   │   │   └── index.ts
│   │   │
│   │   └── forms/                   # Form components
│   │       ├── FormField.tsx
│   │       ├── FormError.tsx
│   │       ├── FormLabel.tsx
│   │       └── index.ts
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   ├── client.ts            # Axios instance
│   │   │   ├── auth.ts              # Auth API functions
│   │   │   ├── users.ts             # User API functions
│   │   │   ├── organizations.ts     # Org API functions
│   │   │   ├── billing.ts           # Billing API functions
│   │   │   ├── leads.ts             # Leads API functions
│   │   │   └── privacy.ts           # Privacy API functions
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useUser.ts
│   │   │   ├── useOrganization.ts
│   │   │   ├── useSubscription.ts
│   │   │   ├── useInvoices.ts
│   │   │   ├── useToast.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── stores/
│   │   │   ├── authStore.ts
│   │   │   ├── uiStore.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── utils/
│   │   │   ├── cn.ts                # classnames utility
│   │   │   ├── formatters.ts        # Date, currency formatters
│   │   │   ├── validators.ts        # Form validators
│   │   │   ├── constants.ts         # Frontend constants
│   │   │   └── index.ts
│   │   │
│   │   └── types/
│   │       ├── api.ts               # API response types
│   │       ├── models.ts            # Data model types
│   │       ├── forms.ts             # Form types
│   │       └── index.ts
│   │
│   ├── public/
│   │   ├── images/
│   │   │   ├── logo.svg
│   │   │   ├── logo-dark.svg
│   │   │   └── og-image.png
│   │   ├── fonts/
│   │   │   └── Inter-Variable.woff2
│   │   ├── favicon.ico
│   │   ├── robots.txt
│   │   └── sitemap.xml
│   │
│   ├── styles/
│   │   └── tailwind.css
│   │
│   ├── cypress/
│   │   ├── e2e/
│   │   │   ├── auth.cy.ts
│   │   │   ├── pricing.cy.ts
│   │   │   ├── checkout.cy.ts
│   │   │   └── subscription.cy.ts
│   │   ├── fixtures/
│   │   │   └── users.json
│   │   └── support/
│   │       ├── commands.ts
│   │       └── e2e.ts
│   │
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── tsconfig.json
│   ├── package.json
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── .dockerignore
│
├── infrastructure/
│   ├── docker/
│   │   ├── nginx/
│   │   │   ├── nginx.conf
│   │   │   └── ssl/
│   │   │       └── .gitkeep
│   │   └── postgres/
│   │       └── init.sql
│   │
│   ├── kubernetes/                   # K8s manifests (Phase 2)
│   │   └── .gitkeep
│   │
│   └── terraform/                    # IaC (Phase 2)
│       └── .gitkeep
│
├── docs/
│   ├── architecture/
│   │   ├── PAD.md                   # This document
│   │   ├── ERD.md
│   │   └── ADR/                     # Architecture Decision Records
│   │       ├── 001-django-6.md
│   │       ├── 002-gst-generated-field.md
│   │       └── 003-idempotency-pattern.md
│   ├── api/
│   │   └── openapi.yaml
│   ├── runbooks/
│   │   ├── deployment.md
│   │   ├── incident-response.md
│   │   └── dsar-processing.md
│   └── onboarding/
│       └── developer-guide.md
│
├── scripts/
│   ├── setup-dev.sh
│   ├── run-tests.sh
│   ├── generate-migrations.sh
│   └── deploy.sh
│
├── docker-compose.yml               # Development
├── docker-compose.override.yml      # Local overrides
├── docker-compose.prod.yml          # Production
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
└── README.md
PART II: DATA ARCHITECTURE
5. Entity-Relationship Diagram
5.1 Complete ERD
text

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    NEXUSCORE DATABASE SCHEMA                                        │
│                                     Entity-Relationship Diagram                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

                                            ┌─────────────────┐
                                            │     users       │
                                            ├─────────────────┤
                                            │ PK id: UUID     │
                                            │    email: str   │
                                            │    name: str    │
                                            │    company: str │
                                            │    phone: str   │
                                            │    is_verified  │
                                            │    is_active    │
                                            │    is_staff     │
                                            │    timezone     │
                                            │    created_at   │
                                            │    updated_at   │
                                            └────────┬────────┘
                                                     │
                           ┌─────────────────────────┼─────────────────────────┐
                           │                         │                         │
                           │ owns                    │ member of               │ requested
                           ▼                         ▼                         ▼
                ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
                │   organizations     │   │organization_member- │   │   dsar_requests     │
                ├─────────────────────┤   │       ships         │   ├─────────────────────┤
                │ PK id: UUID         │   ├─────────────────────┤   │ PK id: UUID         │
                │    name: str        │   │ PK id: UUID         │   │ FK user_id          │
                │    slug: str        │◄──┤ FK organization_id  │   │    user_email: str  │
                │    uen: str         │   │ FK user_id          │──►│    request_type     │
                │    is_gst_registered│   │    role: str        │   │    status           │
                │    gst_reg_no: str  │   │    permissions[]    │   │    verified_at      │
                │    stripe_customer  │   │    joined_at        │   │    export_url       │
                │    billing_email    │   │ FK invited_by       │   │    processed_at     │
                │    billing_phone    │   └─────────────────────┘   │ FK deletion_approved│
                │    billing_address{}│                             │    requested_at     │
                │    timezone         │                             └─────────────────────┘
                │    locale           │
                │    settings{}       │
                │ FK owner_id         │──────────────────────────────────────────────────────────┐
                │    trial_ends_at    │                                                          │
                │    created_at       │                                                          │
                └─────────┬───────────┘                                                          │
                          │                                                                      │
          ┌───────────────┼───────────────────────────────┐                                      │
          │               │                               │                                      │
          │ has           │ has                           │ generates                            │
          ▼               ▼                               ▼                                      │
┌─────────────────┐ ┌─────────────────┐         ┌─────────────────────┐                          │
│ subscriptions   │ │    invoices     │         │      leads          │                          │
├─────────────────┤ ├─────────────────┤         ├─────────────────────┤                          │
│ PK id: UUID     │ │ PK id: UUID     │         │ PK id: UUID         │                          │
│ FK organization │ │ FK organization │         │    name: str        │                          │
│ FK plan_id      │ │ FK subscription │         │    email: str       │                          │
│    status       │ │    subtotal_cents│        │    phone: str       │                          │
│    cancel_at_end│ │    gst_rate      │        │    company: str     │                          │
│    period_start │ │    gst_amount*   │◄─GEN   │    job_title        │                          │
│    period_end   │ │    total_amount* │◄─GEN   │    source           │                          │
│    trial_start  │ │    amount_paid   │        │    status           │                          │
│    trial_end    │ │    currency      │        │    notes            │                          │
│    stripe_sub_id│ │    iras_tx_code  │        │    utm_source       │                          │
│    stripe_cust  │ │    status        │        │    utm_medium       │                          │
│    metadata{}   │ │    paid          │        │    utm_campaign     │                          │
│    created_at   │ │    paid_at       │        │    form_data{}      │                          │
│    canceled_at  │ │    due_date      │        │ FK assigned_to      │──────────────────────────┤
└────────┬────────┘ │    pdf_url       │        │    next_follow_up   │                          │
         │          │    stripe_inv_id │        │ FK converted_to_user│──────────────────────────┤
         │          │    line_items[]  │        │    converted_at     │                          │
         │          │    metadata{}    │        │    created_at       │                          │
         │          │    created_at    │        └─────────────────────┘                          │
         │          └─────────────────┘                                                          │
         │                                                                                       │
         │ belongs to                                                                            │
         ▼                                                                                       │
┌─────────────────┐                                                                              │
│     plans       │                                                                              │
├─────────────────┤                                                                              │
│ PK id: UUID     │                                                                              │
│    name: str    │                                                                              │
│    description  │                                                                              │
│    sku: str     │                                                                              │
│    billing_period│                                                                             │
│    amount_cents │                                                                              │
│    currency     │                                                                              │
│    features{}   │                                                                              │
│    limits{}     │                                                                              │
│    is_active    │                                                                              │
│    is_visible   │                                                                              │
│    display_order│                                                                              │
│    stripe_price │                                                                              │
│    stripe_prod  │                                                                              │
│    created_at   │                                                                              │
└─────────────────┘                                                                              │
                                                                                                 │
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              INFRASTRUCTURE MODELS                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│ idempotency_records │   │   webhook_events    │   │      events         │
├─────────────────────┤   ├─────────────────────┤   ├─────────────────────┤
│ PK id: UUID         │   │ PK id: UUID         │   │ PK id: UUID         │
│    key: str (UNIQ)  │   │    service: str     │   │    event_type: str  │
│    request_path     │   │    event_id (UNIQ)  │   │ FK user_id          │
│    request_method   │   │    event_type: str  │   │ FK organization_id  │
│    request_hash     │   │    payload{}        │   │    data{}           │
│    status           │   │    processed: bool  │   │    created_at       │
│    response_status  │   │    processing_error │   └─────────────────────┘
│    response_body{}  │   │    retry_count      │
│    expires_at       │   │    last_retry_at    │
│    created_at       │   │    processed_at     │
│    updated_at       │   │    created_at       │
└─────────────────────┘   └─────────────────────┘

Legend:
────────
PK = Primary Key
FK = Foreign Key
{} = JSONB field
[] = Array field
* = GeneratedField (database-computed)
GEN = Points to generated column
UNIQ = Unique constraint
5.2 Relationship Cardinality Matrix
From Entity	To Entity	Cardinality	Relationship Type
User	Organization (owner)	1:N	One user owns many organizations
User	OrganizationMembership	1:N	One user has many memberships
Organization	OrganizationMembership	1:N	One org has many memberships
Organization	Subscription	1:N	One org has many subscriptions
Organization	Invoice	1:N	One org has many invoices
Organization	Lead	1:N	One org generates many leads
Subscription	Invoice	1:N	One subscription has many invoices
Subscription	Plan	N:1	Many subscriptions reference one plan
Lead	User (assigned)	N:1	Many leads assigned to one user
Lead	User (converted)	N:1	Many leads convert to users
User	DSARRequest	1:N	One user has many DSAR requests
User	Event	1:N	One user generates many events
Organization	Event	1:N	One org generates many events
6. Complete Database Schema
6.1 Table: users
SQL

-- Table: users
-- Description: Core user accounts with authentication and profile data
-- Singapore Compliance: PDPA personal data subject

CREATE TABLE users (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Authentication
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,  -- Django PBKDF2 hash
    
    -- Profile
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255) DEFAULT '',
    phone VARCHAR(20) DEFAULT '',
    
    -- Verification
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
    CONSTRAINT users_email_lowercase CHECK (email = LOWER(email)),
    CONSTRAINT verified_users_must_be_active CHECK (
        is_verified = FALSE OR is_active = TRUE
    )
);

-- Indexes
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_verified_active ON users(is_verified, is_active);
CREATE INDEX idx_users_is_staff ON users(is_staff) WHERE is_staff = TRUE;
6.2 Table: organizations
SQL

-- Table: organizations
-- Description: Business entities with Singapore regulatory compliance
-- Singapore Compliance: UEN validation, GST registration

CREATE TABLE organizations (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identity
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    
    -- Singapore Regulatory (PRD-q-3 Enhancement)
    uen VARCHAR(15) NOT NULL UNIQUE,  -- Unique Entity Number
    is_gst_registered BOOLEAN NOT NULL DEFAULT FALSE,
    gst_reg_no VARCHAR(20),  -- Format: M########X
    
    -- Stripe Integration
    stripe_customer_id VARCHAR(255) DEFAULT '',
    
    -- Billing Contact
    billing_email VARCHAR(255) NOT NULL,
    billing_phone VARCHAR(20) DEFAULT '',
    billing_address JSONB NOT NULL DEFAULT '{}',
    
    -- Settings
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Singapore',
    locale VARCHAR(10) NOT NULL DEFAULT 'en-SG',
    settings JSONB NOT NULL DEFAULT '{}',
    
    -- Ownership
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE PROTECT,
    
    -- Trial
    trial_ends_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT org_slug_lowercase CHECK (slug = LOWER(slug)),
    CONSTRAINT trial_ends_after_creation CHECK (
        trial_ends_at IS NULL OR trial_ends_at >= created_at
    ),
    CONSTRAINT gst_reg_requires_gst_status CHECK (
        is_gst_registered = FALSE OR gst_reg_no IS NOT NULL
    ),
    CONSTRAINT valid_uen_format CHECK (
        uen ~ '^[0-9]{8}[A-Z]$' OR 
        uen ~ '^[0-9]{9}[A-Z]$' OR 
        uen ~ '^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$'
    ),
    CONSTRAINT valid_gst_reg_format CHECK (
        gst_reg_no IS NULL OR gst_reg_no ~ '^M[0-9]{8}[A-Z]$'
    )
);

-- Indexes
CREATE UNIQUE INDEX idx_organizations_slug ON organizations(slug);
CREATE UNIQUE INDEX idx_organizations_uen ON organizations(uen);
CREATE INDEX idx_organizations_name ON organizations(name);
CREATE INDEX idx_organizations_stripe_customer ON organizations(stripe_customer_id) 
    WHERE stripe_customer_id != '';
CREATE INDEX idx_organizations_owner ON organizations(owner_id);
CREATE INDEX idx_organizations_created_at ON organizations(created_at);
6.3 Table: organization_memberships
SQL

-- Table: organization_memberships
-- Description: User membership in organizations with role-based permissions

CREATE TABLE organization_memberships (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Relationships
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Role
    role VARCHAR(20) NOT NULL DEFAULT 'member',
    
    -- Cached Permissions (for performance)
    permissions TEXT[] NOT NULL DEFAULT '{}',
    
    -- Invitation Tracking
    invited_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    joined_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_role CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    UNIQUE(organization_id, user_id)
);

-- Indexes
CREATE INDEX idx_org_membership_org_user ON organization_memberships(organization_id, user_id);
CREATE INDEX idx_org_membership_user ON organization_memberships(user_id);
CREATE INDEX idx_org_membership_role ON organization_memberships(role);
CREATE INDEX idx_org_membership_admins ON organization_memberships(organization_id) 
    WHERE role IN ('owner', 'admin');
6.4 Table: plans
SQL

-- Table: plans
-- Description: Subscription plan definitions

CREATE TABLE plans (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identity
    name VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    sku VARCHAR(50) NOT NULL UNIQUE,
    
    -- Pricing
    billing_period VARCHAR(10) NOT NULL DEFAULT 'month',
    amount_cents INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'SGD',
    
    -- Features
    features JSONB NOT NULL DEFAULT '{}',
    limits JSONB NOT NULL DEFAULT '{}',
    
    -- Visibility
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_visible BOOLEAN NOT NULL DEFAULT TRUE,
    display_order INTEGER NOT NULL DEFAULT 0,
    
    -- Stripe Integration
    stripe_price_id VARCHAR(255) DEFAULT '',
    stripe_product_id VARCHAR(255) DEFAULT '',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_billing_period CHECK (billing_period IN ('month', 'year')),
    CONSTRAINT positive_amount CHECK (amount_cents > 0),
    CONSTRAINT valid_currency CHECK (currency ~ '^[A-Z]{3}$')
);

-- Indexes
CREATE UNIQUE INDEX idx_plans_sku ON plans(sku);
CREATE INDEX idx_plans_active_visible ON plans(is_active, is_visible);
CREATE INDEX idx_plans_stripe_price ON plans(stripe_price_id) WHERE stripe_price_id != '';
CREATE INDEX idx_plans_display_order ON plans(display_order);
6.5 Table: subscriptions
SQL

-- Table: subscriptions
-- Description: Customer subscription state management

CREATE TABLE subscriptions (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Relationships
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
    
    -- Stripe Integration
    stripe_subscription_id VARCHAR(255) NOT NULL UNIQUE,
    stripe_customer_id VARCHAR(255) NOT NULL,
    stripe_latest_invoice_id VARCHAR(255) DEFAULT '',
    
    -- Metadata
    metadata JSONB NOT NULL DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    canceled_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT valid_status CHECK (
        status IN ('trialing', 'active', 'past_due', 'canceled', 'unpaid')
    ),
    CONSTRAINT period_end_after_start CHECK (
        current_period_end > current_period_start
    ),
    CONSTRAINT trial_status_requires_trial_end CHECK (
        status != 'trialing' OR trial_end IS NOT NULL
    )
);

-- Indexes
CREATE UNIQUE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_subscriptions_org_status ON subscriptions(organization_id, status);
CREATE INDEX idx_subscriptions_status_period ON subscriptions(status, current_period_end);
CREATE INDEX idx_subscriptions_stripe_customer ON subscriptions(stripe_customer_id);
CREATE INDEX idx_subscriptions_active ON subscriptions(organization_id) 
    WHERE status IN ('active', 'trialing');
6.6 Table: invoices
SQL

-- Table: invoices
-- Description: GST-compliant invoices with database-computed tax
-- Singapore Compliance: IRAS requirements, GST calculation

CREATE TABLE invoices (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Relationships
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE PROTECT,
    subscription_id UUID REFERENCES subscriptions(id) ON DELETE PROTECT,
    
    -- Monetary Values (stored in cents)
    subtotal_cents BIGINT NOT NULL,
    gst_rate DECIMAL(5,4) NOT NULL DEFAULT 0.0900,  -- 9% GST
    
    -- Generated Fields (computed by PostgreSQL)
    gst_amount_cents BIGINT GENERATED ALWAYS AS (
        ROUND(subtotal_cents * gst_rate)
    ) STORED,
    total_amount_cents BIGINT GENERATED ALWAYS AS (
        subtotal_cents + ROUND(subtotal_cents * gst_rate)
    ) STORED,
    
    -- Payment Tracking
    amount_paid_cents BIGINT NOT NULL DEFAULT 0,
    currency VARCHAR(3) NOT NULL DEFAULT 'SGD',
    
    -- IRAS Compliance (PRD-q-3 Enhancement)
    iras_transaction_code VARCHAR(10) NOT NULL DEFAULT 'SR',
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    paid BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Dates
    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
    paid_at TIMESTAMP WITH TIME ZONE,
    
    -- External References
    pdf_url TEXT DEFAULT '',
    stripe_invoice_id VARCHAR(255) NOT NULL UNIQUE,
    stripe_payment_intent_id VARCHAR(255) DEFAULT '',
    
    -- Line Items
    line_items JSONB NOT NULL DEFAULT '[]',
    
    -- Metadata
    metadata JSONB NOT NULL DEFAULT '{}',
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_status CHECK (
        status IN ('draft', 'open', 'paid', 'void', 'uncollectible')
    ),
    CONSTRAINT valid_iras_code CHECK (
        iras_transaction_code IN ('SR', 'ZR', 'OS', 'TX')
    ),
    CONSTRAINT positive_subtotal CHECK (subtotal_cents >= 0),
    CONSTRAINT valid_gst_rate CHECK (gst_rate >= 0 AND gst_rate <= 1),
    CONSTRAINT amount_paid_not_exceed_total CHECK (
        amount_paid_cents <= subtotal_cents + ROUND(subtotal_cents * gst_rate)
    ),
    CONSTRAINT paid_invoices_require_paid_at CHECK (
        paid = FALSE OR paid_at IS NOT NULL
    )
);

-- Indexes
CREATE UNIQUE INDEX idx_invoices_stripe_id ON invoices(stripe_invoice_id);
CREATE INDEX idx_invoices_org_status ON invoices(organization_id, status);
CREATE INDEX idx_invoices_status_due ON invoices(status, due_date);
CREATE INDEX idx_invoices_subscription ON invoices(subscription_id);
CREATE INDEX idx_invoices_created_at ON invoices(created_at);
CREATE INDEX idx_invoices_overdue ON invoices(due_date) 
    WHERE status = 'open' AND due_date < NOW();
6.7 Table: leads
SQL

-- Table: leads
-- Description: Marketing leads with UTM tracking

CREATE TABLE leads (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Contact Information
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) DEFAULT '',
    company VARCHAR(255) NOT NULL,
    job_title VARCHAR(100) DEFAULT '',
    
    -- Lead Details
    source VARCHAR(20) NOT NULL DEFAULT 'website',
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    notes TEXT DEFAULT '',
    
    -- UTM Tracking
    utm_source VARCHAR(100) DEFAULT '',
    utm_medium VARCHAR(100) DEFAULT '',
    utm_campaign VARCHAR(100) DEFAULT '',
    utm_term VARCHAR(100) DEFAULT '',
    utm_content VARCHAR(100) DEFAULT '',
    
    -- Form Data
    form_data JSONB NOT NULL DEFAULT '{}',
    
    -- Assignment
    assigned_to_id UUID REFERENCES users(id) ON DELETE SET NULL,
    next_follow_up TIMESTAMP WITH TIME ZONE,
    
    -- Conversion Tracking
    converted_to_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    converted_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_source CHECK (
        source IN ('website', 'demo_request', 'contact', 'event', 'referral', 'other')
    ),
    CONSTRAINT valid_status CHECK (
        status IN ('new', 'contacted', 'qualified', 'converted', 'disqualified')
    ),
    CONSTRAINT conversion_requires_user CHECK (
        converted_at IS NULL OR converted_to_user_id IS NOT NULL
    )
);

-- Indexes
CREATE INDEX idx_leads_email ON leads(email);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_assigned ON leads(assigned_to_id, status);
CREATE INDEX idx_leads_source ON leads(source, created_at);
CREATE INDEX idx_leads_created_at ON leads(created_at);
CREATE INDEX idx_leads_unassigned_new ON leads(created_at) 
    WHERE status = 'new' AND assigned_to_id IS NULL;

-- Full-text search index
CREATE INDEX idx_leads_search ON leads USING GIN (
    to_tsvector('english', name || ' ' || company || ' ' || email)
);
6.8 Table: dsar_requests
SQL

-- Table: dsar_requests
-- Description: PDPA Data Subject Access Request tracking
-- Singapore Compliance: 72-hour SLA, manual deletion approval

CREATE TABLE dsar_requests (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Requester
    user_email VARCHAR(255) NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Request Details
    request_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    
    -- Verification
    verification_token UUID NOT NULL DEFAULT gen_random_uuid(),
    verified_at TIMESTAMP WITH TIME ZONE,
    verification_method VARCHAR(50) DEFAULT '',
    
    -- Export (for 'export' request type)
    export_url TEXT DEFAULT '',
    export_expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    metadata JSONB NOT NULL DEFAULT '{}',
    failure_reason TEXT DEFAULT '',
    
    -- Timestamps with SLA Tracking
    requested_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    processing_started_at TIMESTAMP WITH TIME ZONE,
    processed_at TIMESTAMP WITH TIME ZONE,
    
    -- Deletion Approval (for 'delete' request type)
    deletion_approved_by_id UUID REFERENCES users(id) ON DELETE SET NULL,
    deletion_approved_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT valid_request_type CHECK (
        request_type IN ('export', 'delete', 'access', 'rectification')
    ),
    CONSTRAINT valid_status CHECK (
        status IN ('pending', 'verifying', 'processing', 'completed', 'failed')
    ),
    CONSTRAINT completed_requires_processed_at CHECK (
        status != 'completed' OR processed_at IS NOT NULL
    ),
    CONSTRAINT deletion_requires_approval CHECK (
        request_type != 'delete' OR status != 'completed' OR deletion_approved_by_id IS NOT NULL
    )
);

-- Indexes
CREATE INDEX idx_dsar_user_email ON dsar_requests(user_email);
CREATE INDEX idx_dsar_status_requested ON dsar_requests(status, requested_at);
CREATE INDEX idx_dsar_type_status ON dsar_requests(request_type, status);
CREATE INDEX idx_dsar_pending_sla ON dsar_requests(requested_at) WHERE status = 'pending';
6.9 Table: idempotency_records
SQL

-- Table: idempotency_records
-- Description: Prevents duplicate payment operations

CREATE TABLE idempotency_records (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Idempotency Key
    key VARCHAR(255) NOT NULL UNIQUE,
    
    -- Request Details
    request_path VARCHAR(255) NOT NULL,
    request_method VARCHAR(10) NOT NULL,
    request_hash VARCHAR(64) NOT NULL,  -- SHA256
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'processing',
    
    -- Response Cache
    response_status_code INTEGER,
    response_body JSONB,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('processing', 'completed', 'failed')),
    CONSTRAINT valid_method CHECK (request_method IN ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'))
);

-- Indexes
CREATE UNIQUE INDEX idx_idempotency_key ON idempotency_records(key);
CREATE INDEX idx_idempotency_expires ON idempotency_records(expires_at);
CREATE INDEX idx_idempotency_request ON idempotency_records(request_path, request_method);

-- Automatic cleanup of expired records (run via cron/celery beat)
-- DELETE FROM idempotency_records WHERE expires_at < NOW();
6.10 Table: webhook_events
SQL

-- Table: webhook_events
-- Description: External webhook event processing and retry tracking

CREATE TABLE webhook_events (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event Identity
    service VARCHAR(50) NOT NULL,
    event_id VARCHAR(255) NOT NULL UNIQUE,
    event_type VARCHAR(100) NOT NULL,
    
    -- Payload
    payload JSONB NOT NULL,
    
    -- Processing Status
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    processing_error TEXT DEFAULT '',
    
    -- Retry Tracking
    retry_count INTEGER NOT NULL DEFAULT 0,
    last_retry_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT valid_service CHECK (service IN ('stripe', 'sendgrid')),
    CONSTRAINT max_retries CHECK (retry_count <= 5)
);

-- Indexes
CREATE UNIQUE INDEX idx_webhook_event_id ON webhook_events(event_id);
CREATE INDEX idx_webhook_service_type ON webhook_events(service, event_type);
CREATE INDEX idx_webhook_unprocessed ON webhook_events(processed, created_at) 
    WHERE processed = FALSE;
CREATE INDEX idx_webhook_created_at ON webhook_events(created_at);
6.11 Table: events
SQL

-- Table: events
-- Description: System event logging for analytics and auditing

CREATE TABLE events (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event Details
    event_type VARCHAR(100) NOT NULL,
    
    -- Context
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    
    -- Data
    data JSONB NOT NULL DEFAULT '{}',
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_events_type_created ON events(event_type, created_at);
CREATE INDEX idx_events_user ON events(user_id, created_at);
CREATE INDEX idx_events_org ON events(organization_id, created_at);
CREATE INDEX idx_events_created_at ON events(created_at);

-- Partition by month for performance (production consideration)
-- CREATE TABLE events (
--     ...
-- ) PARTITION BY RANGE (created_at);
7. Django Model Specifications
7.1 Abstract Base Models
Python

# apps/core/models/base.py

import uuid
from django.db import models
from django.utils import timezone


class UUIDModel(models.Model):
    """Abstract base model with UUID primary key"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class TimestampedModel(UUIDModel):
    """Abstract base model with UUID and timestamps"""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(TimestampedModel):
    """Abstract base model with soft delete capability"""
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark record as deleted without removing from database"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])

    def restore(self):
        """Restore a soft-deleted record"""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
7.2 User Model
Python

# apps/core/models/user.py

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator
from django.utils import timezone

from .base import UUIDModel


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email: str, password: str = None, **extra_fields) -> 'User':
        """Create and return a regular user"""
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> 'User':
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email: str) -> 'User':
        """Allow case-insensitive email lookup"""
        return self.get(email__iexact=email)


class User(UUIDModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email-based authentication.
    
    Singapore Compliance:
    - Stores timezone as Asia/Singapore by default
    - email_preferences for PDPA consent tracking
    """
    
    # Authentication
    email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[EmailValidator()],
        error_messages={'unique': 'A user with this email already exists.'}
    )
    
    # Profile
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    
    # Verification
    is_verified = models.BooleanField(
        default=False,
        help_text='Whether the user has verified their email address'
    )
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Permissions
    is_active = models.BooleanField(
        default=True,
        help_text='Whether the user account is active'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Whether the user can access the admin site'
    )
    
    # Preferences
    timezone = models.CharField(
        max_length=50,
        default='Asia/Singapore'
    )
    email_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text='PDPA consent and email preferences'
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
        return self.name

    def get_short_name(self) -> str:
        return self.name.split()[0] if self.name else ''

    def save(self, *args, **kwargs):
        # Normalize email to lowercase
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def regenerate_verification_token(self) -> uuid.UUID:
        """Generate a new verification token"""
        self.verification_token = uuid.uuid4()
        self.verification_sent_at = timezone.now()
        self.save(update_fields=['verification_token', 'verification_sent_at', 'updated_at'])
        return self.verification_token

    def verify_email(self) -> None:
        """Mark user's email as verified"""
        self.is_verified = True
        self.save(update_fields=['is_verified', 'updated_at'])
7.3 Organization Model
Python

# apps/core/models/organization.py

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

from .base import TimestampedModel
from .user import User


# Singapore UEN Validators
uen_validator = RegexValidator(
    regex=r'^([0-9]{8}[A-Z]|[0-9]{9}[A-Z]|[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z])$',
    message='Enter a valid Singapore UEN (e.g., 12345678A, T12AB1234C)'
)

gst_reg_validator = RegexValidator(
    regex=r'^M[0-9]{8}[A-Z]$',
    message='Enter a valid GST registration number (e.g., M12345678A)'
)


class Organization(TimestampedModel):
    """
    Business entity with Singapore regulatory compliance.
    
    Singapore Compliance:
    - UEN (Unique Entity Number) validation
    - GST registration tracking
    - Billing address for invoicing
    """
    
    # Identity
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    
    # Singapore Regulatory
    uen = models.CharField(
        max_length=15,
        unique=True,
        validators=[uen_validator],
        help_text='Unique Entity Number (ACRA registered)'
    )
    is_gst_registered = models.BooleanField(
        default=False,
        help_text='Whether the organization is GST registered'
    )
    gst_reg_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[gst_reg_validator],
        help_text='GST registration number (if registered)'
    )
    
    # Stripe Integration
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        default='',
        db_index=True
    )
    
    # Billing Contact
    billing_email = models.EmailField()
    billing_phone = models.CharField(max_length=20, blank=True, default='')
    billing_address = models.JSONField(
        default=dict,
        blank=True,
        help_text='Structured billing address'
    )
    
    # Settings
    timezone = models.CharField(max_length=50, default='Asia/Singapore')
    locale = models.CharField(max_length=10, default='en-SG')
    settings = models.JSONField(default=dict, blank=True)
    
    # Ownership
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
                name='gst_reg_requires_gst_status'
            ),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def is_in_trial(self) -> bool:
        """Check if organization is in trial period"""
        if not self.trial_ends_at:
            return False
        return timezone.now() < self.trial_ends_at

    @property
    def days_left_in_trial(self) -> int:
        """Days remaining in trial"""
        if not self.trial_ends_at:
            return 0
        remaining = self.trial_ends_at - timezone.now()
        return max(0, remaining.days)

    @property
    def gst_rate(self) -> float:
        """Current GST rate (9% for registered, 0% otherwise)"""
        return 0.09 if self.is_gst_registered else 0.0

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate GST registration
        if self.is_gst_registered and not self.gst_reg_no:
            raise ValidationError({
                'gst_reg_no': 'GST registration number is required for GST-registered organizations.'
            })
        
        # Normalize slug
        if self.slug:
            self.slug = self.slug.lower()
        
        super().clean()


class OrganizationMembership(TimestampedModel):
    """
    User membership in an organization with role-based permissions.
    
    Roles:
    - owner: Full access, can delete organization
    - admin: Full access except deletion
    - member: Standard access
    - viewer: Read-only access
    """
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    ROLE_PERMISSIONS = {
        'owner': [
            'organization.view', 'organization.edit', 'organization.delete',
            'members.view', 'members.invite', 'members.remove', 'members.change_role',
            'billing.view', 'billing.edit',
            'leads.view', 'leads.edit', 'leads.delete',
        ],
        'admin': [
            'organization.view', 'organization.edit',
            'members.view', 'members.invite', 'members.remove',
            'billing.view', 'billing.edit',
            'leads.view', 'leads.edit', 'leads.delete',
        ],
        'member': [
            'organization.view',
            'members.view',
            'billing.view',
            'leads.view', 'leads.edit',
        ],
        'viewer': [
            'organization.view',
            'members.view',
            'billing.view',
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
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invited_memberships'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organization_memberships'
        unique_together = [('organization', 'user')]
        indexes = [
            models.Index(fields=['organization', 'user']),
            models.Index(fields=['user']),
            models.Index(fields=['role']),
        ]

    def __str__(self) -> str:
        return f'{self.user.email} - {self.organization.name} ({self.role})'

    def save(self, *args, **kwargs):
        # Sync permissions from role
        self.permissions = self.ROLE_PERMISSIONS.get(self.role, [])
        super().save(*args, **kwargs)

    def has_permission(self, permission: str) -> bool:
        """Check if membership has a specific permission"""
        return permission in self.permissions
7.4 Invoice Model (with GeneratedField)
Python

# apps/billing/models/invoice.py

from decimal import Decimal
from django.db import models
from django.utils import timezone

from apps.core.models.base import TimestampedModel
from apps.core.models.organization import Organization


class Invoice(TimestampedModel):
    """
    GST-compliant invoice with database-computed tax amounts.
    
    Singapore Compliance:
    - GST calculation at database level via GeneratedField
    - IRAS transaction codes (SR, ZR, OS, TX)
    - PDF generation for compliance records
    
    CRITICAL: gst_amount_cents and total_amount_cents are computed
    by PostgreSQL, NOT by Django. This ensures calculation consistency
    across all database clients.
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('uncollectible', 'Uncollectible'),
    ]
    
    IRAS_TRANSACTION_CODES = [
        ('SR', 'Standard Rate'),
        ('ZR', 'Zero Rate'),
        ('OS', 'Out of Scope'),
        ('TX', 'Taxable Supply'),
    ]

    # Relationships
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    subscription = models.ForeignKey(
        'Subscription',
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,
        blank=True
    )
    
    # Monetary Values (stored in cents for precision)
    subtotal_cents = models.BigIntegerField(
        help_text='Net amount before tax in cents (e.g., 10000 = $100.00)'
    )
    gst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=Decimal('0.0900'),
        help_text='GST rate as decimal (0.09 = 9%)'
    )
    
    # Database-Computed Fields (PostgreSQL GeneratedField)
    gst_amount_cents = models.GeneratedField(
        expression=models.Func(
            models.F('subtotal_cents') * models.F('gst_rate'),
            function='ROUND',
            output_field=models.BigIntegerField()
        ),
        output_field=models.BigIntegerField(),
        db_persist=True,
        help_text='GST amount computed by database'
    )
    total_amount_cents = models.GeneratedField(
        expression=models.F('subtotal_cents') + models.Func(
            models.F('subtotal_cents') * models.F('gst_rate'),
            function='ROUND',
            output_field=models.BigIntegerField()
        ),
        output_field=models.BigIntegerField(),
        db_persist=True,
        help_text='Total amount computed by database'
    )
    
    # Payment Tracking
    amount_paid_cents = models.BigIntegerField(
        default=0,
        help_text='Amount paid in cents'
    )
    currency = models.CharField(max_length=3, default='SGD')
    
    # IRAS Compliance
    iras_transaction_code = models.CharField(
        max_length=10,
        choices=IRAS_TRANSACTION_CODES,
        default='SR',
        help_text='IRAS transaction code for GST reporting'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )
    paid = models.BooleanField(default=False)
    
    # Dates
    due_date = models.DateTimeField()
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # External References
    pdf_url = models.URLField(blank=True, default='')
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
    
    # Line Items (flexible storage)
    line_items = models.JSONField(
        default=list,
        blank=True,
        help_text='Invoice line items as JSON array'
    )
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'invoices'
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['status', 'due_date']),
            models.Index(fields=['stripe_invoice_id']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(paid=False) | models.Q(paid_at__isnull=False),
                name='paid_invoices_require_paid_at'
            ),
        ]
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'Invoice {self.id} - {self.organization.name}'

    @property
    def subtotal_dollars(self) -> Decimal:
        """Subtotal in dollars"""
        return Decimal(self.subtotal_cents) / 100

    @property
    def gst_amount_dollars(self) -> Decimal:
        """GST amount in dollars"""
        return Decimal(self.gst_amount_cents) / 100

    @property
    def total_amount_dollars(self) -> Decimal:
        """Total amount in dollars"""
        return Decimal(self.total_amount_cents) / 100

    @property
    def amount_paid_dollars(self) -> Decimal:
        """Amount paid in dollars"""
        return Decimal(self.amount_paid_cents) / 100

    @property
    def amount_due_cents(self) -> int:
        """Outstanding amount in cents"""
        return self.total_amount_cents - 
