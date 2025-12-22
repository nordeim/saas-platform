Project Requirements Document (PRD)
TechFlow Solutions - Enterprise SaaS Platform
Version 2.0 | December 22, 2025
Pragmatic Implementation with Django 6.0
Document Control
Attribute	Value
Version	2.0
Status	Draft
Created	December 22, 2025
Framework	Django 6.0 (Released December 3, 2025)
Language	English Only
Target Market	Singapore Enterprise & SMB
Table of Contents
Executive Summary
Business Requirements
Technical Architecture
Database Architecture
Backend Architecture
Frontend Architecture
Security Architecture
Infrastructure & Deployment
Singapore Compliance
Testing Strategy
Project Timeline
Budget & Resources
Risk Management
Appendices
1. Executive Summary
1.1 Project Overview
TechFlow Solutions is building a unified SaaS platform for enterprise workflow automation, targeting the Singapore market. This document defines a pragmatic, achievable implementation using Django 6.0's latest features while maintaining strict compliance with Singapore's regulatory requirements.

1.2 Design Philosophy
text

┌─────────────────────────────────────────────────────────────────┐
│                    PRAGMATIC DESIGN PRINCIPLES                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. START SIMPLE, SCALE SMART                                    │
│     → Monolith first, extract services when proven necessary     │
│                                                                  │
│  2. LEVERAGE DJANGO 6.0                                          │
│     → Built-in Tasks (reduce Celery dependency)                  │
│     → Native CSP support (better security, less config)          │
│     → Template Partials (cleaner email templates)                │
│                                                                  │
│  3. SINGAPORE-FIRST COMPLIANCE                                   │
│     → PDPA built into core, not bolted on                        │
│     → PayNow as primary payment, Stripe as secondary             │
│                                                                  │
│  4. COST-CONSCIOUS INFRASTRUCTURE                                │
│     → Phase 1: $200/month infrastructure                         │
│     → Scale investment with revenue                              │
│                                                                  │
│  5. SHIP FAST, ITERATE FASTER                                    │
│     → MVP in 10 weeks, not 6 months                              │
│     → Feature flags for progressive rollout                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
1.3 Key Objectives
Objective	Target	Measurement
Time to MVP	10 weeks	Feature-complete beta launch
Infrastructure Cost	< $250/month	Phase 1 operational cost
Page Load Time	< 2 seconds	Core Web Vitals (LCP)
PDPA Compliance	100%	Pre-launch audit pass
API Response Time	< 200ms (p95)	Production monitoring
Uptime Target	99.9%	Monthly SLA
1.4 What's Different in This Version
Previous PRD Issue	This Version's Solution
Django 6.0 doesn't exist (was 5.x)	Corrected: Using actual Django 6.0 (Dec 2025)
Over-engineered microservices	Smart monolith with clear module boundaries
Celery for all async work	Django 6.0 built-in Tasks for simple jobs
Socket.IO with Django Channels	Django Channels with native WebSocket
Missing PDPA compliance depth	PDPA as core feature, not afterthought
Stripe-only payments	PayNow primary, Stripe secondary
Kubernetes from day 1	Docker Compose → ECS/Kubernetes later
$2,500/month infrastructure	$200/month Phase 1 target
6-month timeline	10-week MVP timeline
2. Business Requirements
2.1 Target Audience
Segment	Size	Primary Needs	Revenue Potential
Singapore SMBs	20-200 employees	Quick setup, local support, affordable	$50-200/month
Singapore Mid-Market	200-1000 employees	Customization, integrations, compliance	$500-2000/month
Singapore Enterprise	1000+ employees	Security, SLA, dedicated support	$5000+/month
2.2 Core Features by Priority
text

PRIORITY 0 (MVP - Week 1-6)
├── User Authentication (JWT + Session)
├── Organization Management
├── Basic Subscription (Free + Paid tiers)
├── PDPA Consent Management
├── Simple Dashboard
└── PayNow + Stripe Payments

PRIORITY 1 (Beta - Week 7-10)
├── Workflow Builder (Basic)
├── Team Management & RBAC
├── Usage Analytics
├── Email Notifications
└── API Key Management

PRIORITY 2 (Post-Launch - Week 11-16)
├── Advanced Workflows
├── Third-party Integrations (Slack, Teams)
├── Advanced Analytics & Reports
├── SingPass Integration
└── Mobile PWA

PRIORITY 3 (Growth - Week 17+)
├── AI-powered Automation
├── Custom Integrations Marketplace
├── White-label Options
└── Multi-region Support
2.3 Subscription Tiers
Tier	Price (SGD)	Users	Features	Target
Free	$0	3	Basic workflows, 100 API calls/day	Trial
Starter	$49/mo	10	Standard workflows, 5K API calls/day	SMB
Professional	$199/mo	50	Advanced workflows, 50K API calls/day	Mid-Market
Enterprise	Custom	Unlimited	Custom, SLA, dedicated support	Enterprise
3. Technical Architecture
3.1 Architecture Overview
mermaid

graph TB
    subgraph "Client Layer"
        BROWSER[Browser - Next.js 15]
        PWA[PWA - Mobile]
    end
    
    subgraph "Edge Layer"
        CF[CloudFlare]
    end
    
    subgraph "Application Layer"
        CADDY[Caddy Reverse Proxy]
        
        subgraph "Django 6.0 Application"
            WSGI[Gunicorn - WSGI]
            ASGI[Daphne - ASGI/WebSocket]
            TASKS[Django Tasks Workers]
        end
        
        NEXT[Next.js SSR]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL 17)]
        REDIS[(Redis 7.2)]
        S3[S3 Storage]
    end
    
    subgraph "External Services"
        PAYNOW[PayNow API]
        STRIPE[Stripe API]
        SENDGRID[SendGrid]
        SENTRY[Sentry]
    end
    
    BROWSER --> CF
    PWA --> CF
    CF --> CADDY
    
    CADDY --> NEXT
    CADDY --> WSGI
    CADDY --> ASGI
    
    WSGI --> PG
    WSGI --> REDIS
    ASGI --> REDIS
    TASKS --> PG
    TASKS --> REDIS
    
    WSGI --> S3
    WSGI --> PAYNOW
    WSGI --> STRIPE
    TASKS --> SENDGRID
    WSGI --> SENTRY
3.2 Technology Stack
Backend Stack (Django 6.0)
Python

# requirements/base.txt
# Django 6.0 Stack - December 2025

# Core Framework
Django==6.0
djangorestframework==3.15.2
django-cors-headers==4.6.0
django-filter==24.3

# Authentication
djangorestframework-simplejwt==5.4.0
django-allauth==65.0.0

# Database
psycopg[binary,pool]==3.2.3

# Cache & Sessions
django-redis==5.4.0

# Background Tasks - Using Django 6.0 built-in + Celery for complex jobs
celery[redis]==5.4.0
django-celery-beat==2.7.0

# WebSocket
channels==4.2.0
channels-redis==4.2.1

# API Documentation
drf-spectacular==0.28.0

# Storage
boto3==1.35.0
django-storages==1.14.4

# Utilities
python-decouple==3.8
Pillow==11.0.0

# Payments
stripe==11.0.0

# Email
sendgrid==6.11.0

# Monitoring
sentry-sdk[django]==2.19.0

# Development
django-debug-toolbar==4.4.0

# Testing
pytest-django==4.9.0
pytest-cov==6.0.0
factory-boy==3.3.1
Frontend Stack
JSON

{
  "name": "techflow-frontend",
  "dependencies": {
    "next": "15.0.0",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "typescript": "5.6.0",
    
    "tailwindcss": "3.4.15",
    "@radix-ui/react-dialog": "1.1.2",
    "@radix-ui/react-dropdown-menu": "2.1.2",
    "@radix-ui/react-tabs": "1.1.1",
    
    "@tanstack/react-query": "5.60.0",
    "zustand": "5.0.0",
    "react-hook-form": "7.53.0",
    "zod": "3.23.8",
    
    "recharts": "2.13.0",
    "framer-motion": "11.11.0",
    "date-fns": "4.1.0",
    "lucide-react": "0.460.0"
  },
  "devDependencies": {
    "@testing-library/react": "16.0.0",
    "jest": "29.7.0",
    "cypress": "13.15.0",
    "eslint": "9.14.0",
    "prettier": "3.4.0"
  }
}
3.3 Project Structure
Bash

techflow/
├── backend/                          # Django 6.0 Application
│   ├── config/                       # Project configuration
│   │   ├── settings/
│   │   │   ├── base.py              # Base settings
│   │   │   ├── development.py       # Dev settings
│   │   │   ├── production.py        # Prod settings
│   │   │   └── testing.py           # Test settings
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── tasks.py                 # Django 6.0 Tasks configuration
│   │
│   ├── apps/
│   │   ├── core/                    # Shared utilities
│   │   │   ├── models.py            # Base models
│   │   │   ├── permissions.py       # Permission classes
│   │   │   ├── middleware.py        # Custom middleware
│   │   │   ├── exceptions.py        # Custom exceptions
│   │   │   └── utils.py
│   │   │
│   │   ├── identity/                # Authentication & Users
│   │   │   ├── models.py            # User, Session models
│   │   │   ├── views.py             # Auth views
│   │   │   ├── serializers.py
│   │   │   ├── tasks.py             # Django 6.0 @task decorated
│   │   │   └── tests/
│   │   │
│   │   ├── organizations/           # Organization Management
│   │   │   ├── models.py            # Organization, Member, Invitation
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py          # Business logic
│   │   │   └── tests/
│   │   │
│   │   ├── billing/                 # Subscriptions & Payments
│   │   │   ├── models.py            # Subscription, Invoice, Payment
│   │   │   ├── views.py
│   │   │   ├── providers/           # Payment providers
│   │   │   │   ├── base.py
│   │   │   │   ├── stripe.py
│   │   │   │   └── paynow.py
│   │   │   ├── tasks.py
│   │   │   └── tests/
│   │   │
│   │   ├── workflows/               # Core Business Logic
│   │   │   ├── models.py            # Workflow, Step, Execution
│   │   │   ├── views.py
│   │   │   ├── engine.py            # Workflow execution engine
│   │   │   ├── tasks.py
│   │   │   └── tests/
│   │   │
│   │   ├── compliance/              # Singapore PDPA Compliance
│   │   │   ├── models.py            # Consent, AccessRequest, Breach
│   │   │   ├── views.py
│   │   │   ├── services.py          # PDPA service layer
│   │   │   ├── tasks.py
│   │   │   └── tests/
│   │   │
│   │   ├── analytics/               # Usage & Reporting
│   │   │   ├── models.py            # UsageRecord, Report
│   │   │   ├── views.py
│   │   │   ├── aggregators.py
│   │   │   └── tests/
│   │   │
│   │   └── notifications/           # Email, Push, In-App
│   │       ├── models.py
│   │       ├── views.py
│   │       ├── channels/
│   │       │   ├── email.py
│   │       │   └── websocket.py
│   │       ├── tasks.py
│   │       └── templates/           # Email templates with partials
│   │           └── email/
│   │
│   ├── api/                         # API versioning
│   │   └── v1/
│   │       ├── urls.py
│   │       └── views.py
│   │
│   ├── templates/                   # Django templates
│   │   ├── email/                   # Email templates
│   │   └── admin/                   # Admin customization
│   │
│   ├── static/
│   ├── media/
│   ├── tests/                       # Integration tests
│   ├── Dockerfile
│   └── manage.py
│
├── frontend/                        # Next.js 15 Application
│   ├── src/
│   │   ├── app/                     # App Router
│   │   │   ├── (marketing)/         # Public pages
│   │   │   ├── (auth)/              # Auth pages
│   │   │   ├── (dashboard)/         # Protected pages
│   │   │   └── api/                 # API routes
│   │   ├── components/
│   │   │   ├── ui/                  # Base components
│   │   │   ├── features/            # Feature components
│   │   │   └── layouts/             # Layout components
│   │   ├── lib/
│   │   │   ├── api/                 # API client
│   │   │   ├── hooks/               # Custom hooks
│   │   │   ├── stores/              # Zustand stores
│   │   │   └── utils/               # Utilities
│   │   └── styles/
│   ├── public/
│   ├── tests/
│   ├── Dockerfile
│   └── package.json
│
├── infrastructure/
│   ├── docker/
│   │   ├── docker-compose.yml       # Local development
│   │   ├── docker-compose.prod.yml  # Production
│   │   └── Caddyfile                # Reverse proxy config
│   ├── scripts/
│   │   ├── deploy.sh
│   │   └── backup.sh
│   └── terraform/                   # Future: IaC
│
├── docs/
│   ├── architecture/
│   ├── api/
│   └── runbooks/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── .env.example
├── Makefile
└── README.md
4. Database Architecture
4.1 Core Schema Design
SQL

-- ============================================
-- TechFlow Database Schema
-- PostgreSQL 17 | Django 6.0
-- ============================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- Fuzzy text search
CREATE EXTENSION IF NOT EXISTS "btree_gist";   -- Exclusion constraints

-- ============================================
-- IDENTITY DOMAIN
-- ============================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Profile
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    display_name VARCHAR(200) GENERATED ALWAYS AS (
        first_name || ' ' || last_name
    ) STORED,
    avatar_url TEXT,
    phone VARCHAR(20),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_staff BOOLEAN DEFAULT false,
    is_superuser BOOLEAN DEFAULT false,
    email_verified BOOLEAN DEFAULT false,
    
    -- Security
    mfa_enabled BOOLEAN DEFAULT false,
    mfa_secret VARCHAR(255),
    password_changed_at TIMESTAMPTZ,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMPTZ,
    
    -- Preferences
    timezone VARCHAR(50) DEFAULT 'Asia/Singapore',
    preferences JSONB DEFAULT '{}',
    
    -- Timestamps
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    -- Soft delete
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET NOT NULL,
    user_agent TEXT,
    device_type VARCHAR(50),  -- 'desktop', 'mobile', 'tablet'
    
    last_activity_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMPTZ
);

-- ============================================
-- ORGANIZATION DOMAIN
-- ============================================

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Basic Info
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    logo_url TEXT,
    
    -- Singapore Business Details
    uen VARCHAR(20),  -- Unique Entity Number
    gst_registered BOOLEAN DEFAULT false,
    gst_number VARCHAR(20),
    
    -- Settings
    timezone VARCHAR(50) DEFAULT 'Asia/Singapore',
    settings JSONB DEFAULT '{}',
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    
    -- UEN validation for Singapore companies
    CONSTRAINT valid_uen CHECK (
        uen IS NULL OR 
        uen ~ '^[0-9]{8}[A-Z]$' OR
        uen ~ '^[0-9]{9}[A-Z]$' OR
        uen ~ '^[TSRF][0-9]{2}[A-Z]{2}[0-9]{4}[A-Z]$'
    )
);

CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    role VARCHAR(20) NOT NULL CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    permissions JSONB DEFAULT '{}',  -- Fine-grained permissions
    
    invited_by UUID REFERENCES users(id),
    invited_at TIMESTAMPTZ,
    joined_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    is_active BOOLEAN DEFAULT true,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(organization_id, user_id)
);

CREATE TABLE organization_invitations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    email VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'member',
    token VARCHAR(255) UNIQUE NOT NULL,
    
    invited_by UUID NOT NULL REFERENCES users(id),
    
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'expired', 'revoked')),
    expires_at TIMESTAMPTZ NOT NULL,
    accepted_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- BILLING DOMAIN
-- ============================================

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID UNIQUE NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    -- Plan Details
    tier VARCHAR(20) NOT NULL CHECK (tier IN ('free', 'starter', 'professional', 'enterprise')),
    status VARCHAR(20) NOT NULL CHECK (status IN ('trialing', 'active', 'past_due', 'canceled', 'paused')),
    
    -- Billing Period
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    trial_end TIMESTAMPTZ,
    
    -- Payment Integration
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    
    -- Plan Limits
    max_users INTEGER NOT NULL DEFAULT 3,
    max_workflows INTEGER NOT NULL DEFAULT 5,
    max_api_calls_daily INTEGER NOT NULL DEFAULT 100,
    max_storage_mb INTEGER NOT NULL DEFAULT 100,
    
    -- Cancellation
    cancel_at_period_end BOOLEAN DEFAULT false,
    canceled_at TIMESTAMPTZ,
    cancellation_reason TEXT,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES subscriptions(id),
    
    -- Invoice Details
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('draft', 'pending', 'paid', 'failed', 'refunded')),
    
    -- Amounts (in cents)
    subtotal_cents INTEGER NOT NULL,
    tax_cents INTEGER NOT NULL DEFAULT 0,
    total_cents INTEGER NOT NULL,
    currency CHAR(3) DEFAULT 'SGD',
    
    -- GST (Singapore)
    gst_rate DECIMAL(5, 4) DEFAULT 0.09,  -- 9% GST
    gst_amount_cents INTEGER DEFAULT 0,
    
    -- Period
    period_start TIMESTAMPTZ,
    period_end TIMESTAMPTZ,
    due_date DATE,
    paid_at TIMESTAMPTZ,
    
    -- Payment Details
    payment_method VARCHAR(50),  -- 'paynow', 'stripe_card', 'bank_transfer'
    payment_reference VARCHAR(255),
    
    -- PDF
    pdf_url TEXT,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    invoice_id UUID REFERENCES invoices(id),
    
    -- Payment Details
    amount_cents INTEGER NOT NULL,
    currency CHAR(3) DEFAULT 'SGD',
    
    -- Provider
    provider VARCHAR(20) NOT NULL CHECK (provider IN ('stripe', 'paynow', 'bank_transfer')),
    provider_payment_id VARCHAR(255),
    
    -- Status
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'refunded')),
    
    -- PayNow Specific
    paynow_qr_data TEXT,
    paynow_reference VARCHAR(50),
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    failure_reason TEXT,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ
);

-- ============================================
-- WORKFLOW DOMAIN
-- ============================================

CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Workflow Definition (JSON Schema)
    definition JSONB NOT NULL DEFAULT '{"nodes": [], "edges": []}',
    version INTEGER DEFAULT 1,
    
    -- Status
    is_published BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    
    -- Ownership
    created_by UUID NOT NULL REFERENCES users(id),
    published_by UUID REFERENCES users(id),
    published_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(organization_id, name)
);

CREATE TABLE workflow_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    -- Execution Details
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'running', 'completed', 'failed', 'canceled')),
    
    -- Input/Output
    input_data JSONB DEFAULT '{}',
    output_data JSONB DEFAULT '{}',
    
    -- Error Handling
    error_message TEXT,
    error_details JSONB,
    
    -- Timing
    started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    duration_ms INTEGER,
    
    -- Trigger
    triggered_by UUID REFERENCES users(id),
    trigger_type VARCHAR(20) CHECK (trigger_type IN ('manual', 'scheduled', 'webhook', 'api')),
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- COMPLIANCE DOMAIN (Singapore PDPA)
-- ============================================

CREATE TABLE pdpa_consents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    
    -- Consent Type
    consent_type VARCHAR(50) NOT NULL CHECK (consent_type IN (
        'terms_of_service',
        'privacy_policy',
        'marketing_email',
        'marketing_sms',
        'marketing_phone',
        'data_analytics',
        'third_party_sharing',
        'cross_border_transfer'
    )),
    
    -- Consent State
    is_granted BOOLEAN NOT NULL,
    granted_at TIMESTAMPTZ,
    withdrawn_at TIMESTAMPTZ,
    
    -- Evidence of Consent
    consent_version VARCHAR(20) NOT NULL,
    consent_text TEXT NOT NULL,  -- Exact text shown
    collection_method VARCHAR(50) NOT NULL,  -- 'web_form', 'api', 'import'
    
    -- Context
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, consent_type)
);

CREATE TABLE pdpa_access_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reference_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Requester
    user_id UUID REFERENCES users(id),
    requester_email VARCHAR(255) NOT NULL,
    requester_name VARCHAR(255) NOT NULL,
    
    -- Request Details
    request_type VARCHAR(20) NOT NULL CHECK (request_type IN ('access', 'correction', 'deletion')),
    request_details TEXT NOT NULL,
    
    -- Status Tracking
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'identity_verification', 'in_progress', 'completed', 'rejected'
    )),
    
    -- PDPA Timeline (30 days)
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    
    -- Response
    response_details TEXT,
    response_documents JSONB DEFAULT '[]',
    
    -- Handling
    assigned_to UUID REFERENCES users(id),
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pdpa_breach_incidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reference_number VARCHAR(50) UNIQUE NOT NULL,
    
    -- Discovery
    detected_at TIMESTAMPTZ NOT NULL,
    detected_by UUID REFERENCES users(id),
    
    -- Classification
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    
    -- Scope
    data_types_affected TEXT[] NOT NULL,
    estimated_individuals INTEGER,
    
    -- PDPC Notification (required within 72 hours for significant breaches)
    pdpc_notification_required BOOLEAN DEFAULT false,
    pdpc_notified_at TIMESTAMPTZ,
    pdpc_reference VARCHAR(100),
    
    -- Status
    status VARCHAR(20) DEFAULT 'investigating' CHECK (status IN (
        'investigating', 'contained', 'remediated', 'closed'
    )),
    
    -- Investigation
    root_cause TEXT,
    remediation_actions JSONB DEFAULT '[]',
    
    description TEXT NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMPTZ
);

-- ============================================
-- ANALYTICS DOMAIN
-- ============================================

CREATE TABLE usage_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    metric_type VARCHAR(50) NOT NULL,  -- 'api_calls', 'storage_mb', 'workflow_executions'
    quantity DECIMAL(12, 4) NOT NULL,
    
    -- Time bucket (for aggregation)
    recorded_date DATE NOT NULL,
    recorded_hour SMALLINT,  -- 0-23, NULL for daily metrics
    
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    
    -- Change Details
    changes JSONB DEFAULT '{}',
    
    -- Context
    ip_address INET,
    user_agent TEXT,
    request_id VARCHAR(100),
    
    -- PDPA: Track personal data access
    personal_data_accessed TEXT[],
    
    -- Tamper-evident hash chain
    previous_hash VARCHAR(64),
    entry_hash VARCHAR(64),
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- NOTIFICATIONS DOMAIN
-- ============================================

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    
    -- Content
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    
    -- Delivery
    channel VARCHAR(20) NOT NULL CHECK (channel IN ('in_app', 'email', 'push')),
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    
    -- Action
    action_url TEXT,
    action_data JSONB DEFAULT '{}',
    
    -- Status
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMPTZ,
    sent_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- API DOMAIN
-- ============================================

CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    
    name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Key (only prefix stored, hash for validation)
    key_prefix VARCHAR(12) NOT NULL,  -- 'tf_live_xxxx'
    key_hash VARCHAR(255) NOT NULL,
    
    -- Scopes
    scopes TEXT[] DEFAULT '{}',
    
    -- Rate Limiting
    rate_limit_per_minute INTEGER DEFAULT 60,
    
    -- Validity
    is_active BOOLEAN DEFAULT true,
    expires_at TIMESTAMPTZ,
    last_used_at TIMESTAMPTZ,
    
    created_by UUID NOT NULL REFERENCES users(id),
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMPTZ,
    revoked_by UUID REFERENCES users(id)
);

-- ============================================
-- INDEXES
-- ============================================

-- Users
CREATE INDEX idx_users_email ON users(LOWER(email)) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_last_login ON users(last_login_at DESC);

-- Sessions
CREATE INDEX idx_sessions_token ON user_sessions(token_hash) WHERE revoked_at IS NULL;
CREATE INDEX idx_sessions_user ON user_sessions(user_id, expires_at DESC);

-- Organizations
CREATE INDEX idx_org_slug ON organizations(slug) WHERE deleted_at IS NULL;
CREATE INDEX idx_org_uen ON organizations(uen) WHERE uen IS NOT NULL;

-- Members
CREATE INDEX idx_members_org ON organization_members(organization_id) WHERE is_active;
CREATE INDEX idx_members_user ON organization_members(user_id) WHERE is_active;

-- Subscriptions
CREATE INDEX idx_subs_org ON subscriptions(organization_id);
CREATE INDEX idx_subs_status ON subscriptions(status, current_period_end);

-- Workflows
CREATE INDEX idx_workflows_org ON workflows(organization_id) WHERE is_active;
CREATE INDEX idx_workflow_exec_status ON workflow_executions(status, created_at DESC);

-- Compliance
CREATE INDEX idx_consents_user ON pdpa_consents(user_id);
CREATE INDEX idx_access_requests_status ON pdpa_access_requests(status, due_date);
CREATE INDEX idx_breach_severity ON pdpa_breach_incidents(severity, status);

-- Analytics
CREATE INDEX idx_usage_org_date ON usage_records(organization_id, recorded_date DESC);
CREATE INDEX idx_audit_org_action ON audit_logs(organization_id, action, created_at DESC);

-- Notifications
CREATE INDEX idx_notifications_user ON notifications(user_id, is_read, created_at DESC);

-- API Keys
CREATE INDEX idx_api_keys_hash ON api_keys(key_hash) WHERE is_active;

-- Full-text search
CREATE INDEX idx_users_search ON users USING gin(
    to_tsvector('english', first_name || ' ' || last_name || ' ' || email)
);
CREATE INDEX idx_org_search ON organizations USING gin(
    to_tsvector('english', name)
);
CREATE INDEX idx_workflows_search ON workflows USING gin(
    to_tsvector('english', name || ' ' || COALESCE(description, ''))
);

-- ============================================
-- TRIGGERS
-- ============================================

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_organizations_updated_at
    BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Auto-set PDPA access request due date (30 days)
CREATE OR REPLACE FUNCTION set_pdpa_due_date()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.due_date IS NULL THEN
        NEW.due_date = NEW.submitted_at + INTERVAL '30 days';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_access_request_due_date
    BEFORE INSERT ON pdpa_access_requests
    FOR EACH ROW EXECUTE FUNCTION set_pdpa_due_date();

-- Generate invoice number
CREATE OR REPLACE FUNCTION generate_invoice_number()
RETURNS TRIGGER AS $$
DECLARE
    year_month TEXT;
    seq_num INTEGER;
BEGIN
    year_month := TO_CHAR(CURRENT_DATE, 'YYYYMM');
    
    SELECT COALESCE(MAX(CAST(SUBSTRING(invoice_number FROM 8) AS INTEGER)), 0) + 1
    INTO seq_num
    FROM invoices
    WHERE invoice_number LIKE 'TF' || year_month || '%';
    
    NEW.invoice_number := 'TF' || year_month || LPAD(seq_num::TEXT, 4, '0');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER generate_invoice_number_trigger
    BEFORE INSERT ON invoices
    FOR EACH ROW
    WHEN (NEW.invoice_number IS NULL)
    EXECUTE FUNCTION generate_invoice_number();
4.2 Data Retention Policy
SQL

-- Data Retention Policies (PDPA Compliant)
CREATE TABLE data_retention_policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    data_category VARCHAR(100) UNIQUE NOT NULL,
    retention_days INTEGER NOT NULL,
    legal_basis TEXT NOT NULL,
    auto_delete BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO data_retention_policies (data_category, retention_days, legal_basis, auto_delete) VALUES
('audit_logs', 2555, 'Legal: 7 years for financial records (IRAS)', false),
('user_sessions', 90, 'Security: Session tracking for incident investigation', true),
('api_logs', 365, 'Operational: Debugging and usage analysis', true),
('pdpa_consents', 2555, 'Legal: Proof of consent required under PDPA', false),
('deleted_users', 30, 'Grace period for account recovery requests', true),
('workflow_executions', 365, 'Business: Historical execution data', true),
('notifications', 90, 'Operational: Read notification cleanup', true),
('usage_records', 730, 'Business: 2 years for billing disputes', false);
5. Backend Architecture
5.1 Django 6.0 Configuration
Python

# config/settings/base.py
"""
Django 6.0 Base Settings
TechFlow Solutions
"""

import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
from django.utils.csp import CSP

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =============================================================================
# CORE SETTINGS
# =============================================================================

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'channels',
    'drf_spectacular',
    'storages',
    'django_celery_beat',
]

LOCAL_APPS = [
    'apps.core',
    'apps.identity',
    'apps.organizations',
    'apps.billing',
    'apps.workflows',
    'apps.compliance',
    'apps.analytics',
    'apps.notifications',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Django 6.0 CSP Middleware
    'django.middleware.security.ContentSecurityPolicyMiddleware',
    
    # Custom Middleware
    'apps.core.middleware.AuditLogMiddleware',
    'apps.core.middleware.OrganizationContextMiddleware',
]

# =============================================================================
# DJANGO 6.0 CONTENT SECURITY POLICY
# =============================================================================

SECURE_CSP = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE],
    "style-src": [CSP.SELF, CSP.UNSAFE_INLINE],  # Required for Tailwind
    "img-src": [CSP.SELF, "https:", "data:"],
    "font-src": [CSP.SELF, "https://fonts.gstatic.com"],
    "connect-src": [
        CSP.SELF, 
        "https://api.stripe.com",
        "wss://*.techflow.sg",
    ],
    "frame-ancestors": [CSP.NONE],
    "form-action": [CSP.SELF],
    "base-uri": [CSP.SELF],
}

# Report-only mode for initial deployment (monitor without blocking)
SECURE_CSP_REPORT_ONLY = {
    **SECURE_CSP,
    "report-uri": "/api/v1/csp-report/",
}

# =============================================================================
# DJANGO 6.0 BACKGROUND TASKS
# =============================================================================

TASKS = {
    "default": {
        "BACKEND": "django.tasks.backends.database.DatabaseBackend",
        "QUEUES": ["default", "high_priority", "low_priority"],
    }
}

# For complex tasks that need Celery (retries, schedules, etc.)
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/1')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/2')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Singapore'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# =============================================================================
# DATABASE
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='techflow'),
        'USER': config('DB_USER', default='techflow'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000',
        },
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CACHE & SESSIONS
# =============================================================================

REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'IGNORE_EXCEPTIONS': True,
        },
        'KEY_PREFIX': 'tf',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400 * 7  # 7 days
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# =============================================================================
# AUTHENTICATION
# =============================================================================

AUTH_USER_MODEL = 'identity.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# REST FRAMEWORK
# =============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# =============================================================================
# JWT SETTINGS
# =============================================================================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# =============================================================================
# CORS
# =============================================================================

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# CHANNELS (WebSocket)
# =============================================================================

ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# =============================================================================
# STATIC & MEDIA
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# EMAIL (Django 6.0 Modern Email API)
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@techflow.sg')

# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Singapore'
USE_I18N = True
USE_TZ = True

# =============================================================================
# SECURITY
# =============================================================================

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# HTTPS settings (enabled in production)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# =============================================================================
# SINGAPORE SPECIFIC
# =============================================================================

SINGAPORE_CONFIG = {
    'COMPANY_UEN': config('COMPANY_UEN', default=''),
    'GST_RATE': 0.09,  # 9% GST
    'DPO_EMAIL': config('DPO_EMAIL', default='dpo@techflow.sg'),
    'PDPA_BREACH_NOTIFICATION_HOURS': 72,
}

# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# =============================================================================
# SENTRY
# =============================================================================

SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,  # PDPA: Don't send PII to Sentry
    )
5.2 Django 6.0 Background Tasks
Python

# apps/notifications/tasks.py
"""
Background Tasks using Django 6.0 Built-in Tasks Framework
"""

from django.tasks import task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@task
def send_email_notification(
    *,  # Django 6.0: keyword-only arguments
    to_email: str,
    subject: str,
    template_name: str,
    context: dict,
) -> bool:
    """
    Send email notification using Django 6.0 task decorator.
    
    Uses Django 6.0's modern email API.
    """
    try:
        # Render template with partials support (Django 6.0)
        html_content = render_to_string(f'email/{template_name}.html', context)
        text_content = render_to_string(f'email/{template_name}.txt', context)
        
        # Create email using Django 6.0 modern API
        email = EmailMessage(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.content_subtype = 'html'
        email.body = html_content
        
        email.send(fail_silently=False)
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


@task
def send_welcome_email(*, user_id: str) -> bool:
    """Send welcome email to new user."""
    from apps.identity.models import User
    
    user = User.objects.get(id=user_id)
    
    return send_email_notification.enqueue(
        to_email=user.email,
        subject="Welcome to TechFlow",
        template_name="welcome",
        context={
            'user_name': user.first_name,
            'login_url': f"{settings.FRONTEND_URL}/login",
        }
    )


@task
def send_invoice_email(*, invoice_id: str) -> bool:
    """Send invoice to organization billing contact."""
    from apps.billing.models import Invoice
    
    invoice = Invoice.objects.select_related(
        'organization', 'subscription'
    ).get(id=invoice_id)
    
    # Get billing contact
    owner = invoice.organization.members.filter(role='owner').first()
    
    if not owner:
        logger.warning(f"No owner found for organization {invoice.organization_id}")
        return False
    
    return send_email_notification.enqueue(
        to_email=owner.user.email,
        subject=f"TechFlow Invoice {invoice.invoice_number}",
        template_name="invoice",
        context={
            'invoice': invoice,
            'organization': invoice.organization,
            'payment_url': f"{settings.FRONTEND_URL}/billing/pay/{invoice.id}",
        }
    )


@task
def process_pdpa_access_request(*, request_id: str) -> dict:
    """
    Process PDPA data access request.
    Compiles all user data for export.
    """
    from apps.compliance.models import PDPAAccessRequest
    from apps.compliance.services import PDPAExportService
    
    access_request = PDPAAccessRequest.objects.get(id=request_id)
    
    # Update status
    access_request.status = 'in_progress'
    access_request.save(update_fields=['status', 'updated_at'])
    
    try:
        export_service = PDPAExportService()
        export_url = export_service.generate_user_data_export(
            user_id=str(access_request.user_id)
        )
        
        access_request.status = 'completed'
        access_request.response_documents = [export_url]
        access_request.completed_at = timezone.now()
        access_request.save()
        
        # Notify user
        send_email_notification.enqueue(
            to_email=access_request.requester_email,
            subject="Your Data Access Request is Complete",
            template_name="pdpa_export_ready",
            context={
                'download_url': export_url,
                'reference': access_request.reference_number,
            }
        )
        
        return {'status': 'completed', 'export_url': export_url}
        
    except Exception as e:
        logger.error(f"PDPA export failed for request {request_id}: {e}")
        access_request.status = 'failed'
        access_request.save(update_fields=['status'])
        raise


@task
def calculate_daily_usage(*, organization_id: str, date: str) -> dict:
    """Calculate and store daily usage metrics."""
    from apps.analytics.services import UsageCalculator
    from datetime import datetime
    
    calc_date = datetime.strptime(date, '%Y-%m-%d').date()
    calculator = UsageCalculator(organization_id)
    
    metrics = calculator.calculate_daily_metrics(calc_date)
    
    logger.info(f"Calculated usage for org {organization_id}: {metrics}")
    return metrics
5.3 Using Django 6.0 Tasks (Enqueueing)
Python

# Example: Enqueuing tasks in views

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.notifications.tasks import send_welcome_email, send_invoice_email


class UserRegistrationView(APIView):
    permission_classes = []
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        # Enqueue welcome email using Django 6.0 Tasks
        send_welcome_email.enqueue(user_id=str(user.id))
        
        return Response(
            {'message': 'Registration successful'},
            status=status.HTTP_201_CREATED
        )


class InvoiceGenerationView(APIView):
    
    def post(self, request, organization_id):
        # Generate invoice
        invoice = Invoice.objects.create(
            organization_id=organization_id,
            # ... other fields
        )
        
        # Enqueue invoice email
        send_invoice_email.enqueue(invoice_id=str(invoice.id))
        
        return Response(
            InvoiceSerializer(invoice).data,
            status=status.HTTP_201_CREATED
        )
5.4 Email Templates with Django 6.0 Partials
HTML

<!-- templates/email/_base.html -->
{% load partials %}

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f5;">
    
    {% partialdef "header" %}
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
        <tr>
            <td style="padding: 24px; text-align: center; background-color: #0066ff;">
                <img src="{{ logo_url }}" alt="TechFlow" height="40">
            </td>
        </tr>
    </table>
    {% endpartialdef %}
    
    {% partialdef "footer" %}
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
        <tr>
            <td style="padding: 24px; text-align: center; background-color: #f4f4f5;">
                <p style="margin: 0 0 8px 0; color: #71717a; font-size: 12px;">
                    TechFlow Solutions Pte Ltd
                </p>
                <p style="margin: 0; color: #71717a; font-size: 12px;">
                    1 Marina Boulevard, Singapore 018989
                </p>
                <p style="margin: 16px 0 0 0;">
                    <a href="{{ unsubscribe_url }}" style="color: #71717a; font-size: 12px;">
                        Unsubscribe
                    </a>
                </p>
            </td>
        </tr>
    </table>
    {% endpartialdef %}
    
    {% partialdef "button" %}
    <table cellpadding="0" cellspacing="0" style="margin: 24px auto;">
        <tr>
            <td style="background-color: #0066ff; padding: 12px 32px; border-radius: 8px;">
                <a href="{{ button_url }}" style="color: #ffffff; text-decoration: none; font-weight: 600;">
                    {{ button_text }}
                </a>
            </td>
        </tr>
    </table>
    {% endpartialdef %}
    
    {% block content %}{% endblock %}
    
</body>
</html>


<!-- templates/email/welcome.html -->
{% extends "email/_base.html" %}

{% block content %}

{% partial "header" %}

<table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
    <tr>
        <td style="padding: 48px 24px;">
            <h1 style="margin: 0 0 16px 0; font-size: 24px; color: #18181b;">
                Welcome to TechFlow, {{ user_name }}!
            </h1>
            
            <p style="margin: 0 0 24px 0; color: #3f3f46; line-height: 1.6;">
                We're excited to have you on board. TechFlow helps you automate 
                your business workflows and boost productivity.
            </p>
            
            <p style="margin: 0 0 24px 0; color: #3f3f46; line-height: 1.6;">
                Here's what you can do next:
            </p>
            
            <ul style="margin: 0 0 24px 0; padding-left: 24px; color: #3f3f46;">
                <li style="margin-bottom: 8px;">Complete your profile</li>
                <li style="margin-bottom: 8px;">Create your first workflow</li>
                <li style="margin-bottom: 8px;">Invite your team members</li>
            </ul>
            
            {% with button_url=login_url button_text="Get Started" %}
                {% partial "button" %}
            {% endwith %}
        </td>
    </tr>
</table>

{% partial "footer" %}

{% endblock %}
5.5 Payment Providers
Python

# apps/billing/providers/paynow.py
"""
PayNow Payment Provider for Singapore
"""

import hashlib
import qrcode
import io
import base64
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .base import PaymentProvider, PaymentResult, PaymentMethod


class PayNowProvider(PaymentProvider):
    """
    PayNow Corporate Payment Integration
    Uses EMVCo QR standard for Singapore
    """
    
    def __init__(self):
        self.uen = settings.SINGAPORE_CONFIG['COMPANY_UEN']
        self.merchant_name = "TechFlow Solutions Pte Ltd"
    
    def create_payment(
        self,
        amount: Decimal,
        reference: str,
        description: str = "",
    ) -> PaymentResult:
        """Generate PayNow QR code for payment."""
        
        if not self.uen:
            raise ValueError("Company UEN not configured")
        
        # Build EMVCo QR payload
        qr_payload = self._build_emv_payload(
            amount=amount,
            reference=reference[:25],  # Max 25 chars
        )
        
        # Generate QR code image
        qr_image_base64 = self._generate_qr_image(qr_payload)
        
        return PaymentResult(
            success=True,
            transaction_id=reference,
            amount=amount,
            currency="SGD",
            method=PaymentMethod.PAYNOW,
            status="pending",
            qr_code_data=qr_image_base64,
            expires_at=timezone.now() + timedelta(minutes=15),
            instructions={
                "step_1": "Open your banking app",
                "step_2": "Select 'Scan & Pay' or 'PayNow'",
                "step_3": "Scan the QR code",
                "step_4": "Confirm the payment",
            }
        )
    
    def _build_emv_payload(self, amount: Decimal, reference: str) -> str:
        """Build EMVCo-compliant PayNow QR string."""
        
        # EMVCo Data Objects for PayNow
        elements = []
        
        # Payload Format Indicator
        elements.append(self._tlv("00", "01"))
        
        # Point of Initiation Method (12 = Dynamic QR)
        elements.append(self._tlv("01", "12"))
        
        # Merchant Account Information (PayNow)
        paynow_data = (
            self._tlv("00", "SG.PAYNOW") +
            self._tlv("01", "2") +  # Proxy Type: 2 = UEN
            self._tlv("02", self.uen) +
            self._tlv("03", "0") +  # Amount Editable: 0 = No
            self._tlv("04", reference)
        )
        elements.append(self._tlv("26", paynow_data))
        
        # Merchant Category Code (0000 = Default)
        elements.append(self._tlv("52", "0000"))
        
        # Transaction Currency (702 = SGD)
        elements.append(self._tlv("53", "702"))
        
        # Transaction Amount
        amount_str = f"{amount:.2f}"
        elements.append(self._tlv("54", amount_str))
        
        # Country Code
        elements.append(self._tlv("58", "SG"))
        
        # Merchant Name
        elements.append(self._tlv("59", self.merchant_name[:25]))
        
        # Merchant City
        elements.append(self._tlv("60", "Singapore"))
        
        # CRC placeholder
        payload = "".join(elements) + "6304"
        
        # Calculate CRC-16 CCITT
        crc = self._calculate_crc16(payload)
        
        return payload + crc
    
    def _tlv(self, tag: str, value: str) -> str:
        """Create TLV (Tag-Length-Value) element."""
        length = f"{len(value):02d}"
        return f"{tag}{length}{value}"
    
    def _calculate_crc16(self, data: str) -> str:
        """Calculate CRC-16 CCITT checksum."""
        crc = 0xFFFF
        for char in data:
            crc ^= ord(char) << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return f"{crc:04X}"
    
    def _generate_qr_image(self, payload: str) -> str:
        """Generate base64-encoded QR code image."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(payload)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def verify_payment(self, transaction_id: str) -> PaymentResult:
        """
        Verify payment status.
        
        Note: PayNow confirmations come via bank webhook,
        not real-time API. This checks our stored status.
        """
        from apps.billing.models import Payment
        
        payment = Payment.objects.filter(
            paynow_reference=transaction_id
        ).first()
        
        if not payment:
            return PaymentResult(
                success=False,
                transaction_id=transaction_id,
                status="not_found",
            )
        
        return PaymentResult(
            success=payment.status == 'completed',
            transaction_id=transaction_id,
            amount=Decimal(payment.amount_cents) / 100,
            currency="SGD",
            method=PaymentMethod.PAYNOW,
            status=payment.status,
        )
6. Frontend Architecture
6.1 Next.js 15 Configuration
TypeScript

// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL,
  },
  
  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.techflow.sg',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
6.2 API Client with WebSocket
TypeScript

// lib/api/client.ts
import axios, { AxiosInstance, AxiosError } from 'axios';
import { useAuthStore } from '@/lib/stores/auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    const organizationId = useAuthStore.getState().currentOrganizationId;
    if (organizationId) {
      config.headers['X-Organization-Id'] = organizationId;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor with token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && originalRequest) {
      try {
        await useAuthStore.getState().refreshToken();
        return api(originalRequest);
      } catch {
        useAuthStore.getState().logout();
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);


// lib/api/websocket.ts
/**
 * WebSocket client compatible with Django Channels
 */
export class TechFlowWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnects = 5;
  private listeners = new Map<string, Set<(data: any) => void>>();
  private messageQueue: Array<{ type: string; data: any }> = [];
  
  constructor(private getToken: () => string | null) {}
  
  connect(path: string): void {
    const token = this.getToken();
    if (!token) {
      console.error('No auth token for WebSocket');
      return;
    }
    
    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}${path}?token=${token}`;
    
    this.ws = new WebSocket(wsUrl);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      
      // Send queued messages
      while (this.messageQueue.length > 0) {
        const msg = this.messageQueue.shift();
        if (msg) this.send(msg.type, msg.data);
      }
    };
    
    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const handlers = this.listeners.get(message.type);
        handlers?.forEach((handler) => handler(message.data));
      } catch (e) {
        console.error('WebSocket message parse error:', e);
      }
    };
    
    this.ws.onclose = () => {
      if (this.reconnectAttempts < this.maxReconnects) {
        this.reconnectAttempts++;
        setTimeout(() => this.connect(path), 1000 * this.reconnectAttempts);
      }
    };
  }
  
  send(type: string, data: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, ...data }));
    } else {
      this.messageQueue.push({ type, data });
    }
  }
  
  on(type: string, handler: (data: any) => void): () => void {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, new Set());
    }
    this.listeners.get(type)!.add(handler);
    
    return () => this.listeners.get(type)?.delete(handler);
  }
  
  disconnect(): void {
    this.ws?.close(1000, 'Client disconnect');
    this.ws = null;
  }
}
6.3 Authentication Store
TypeScript

// lib/stores/auth.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '@/lib/api/client';

interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  displayName: string;
  avatarUrl?: string;
}

interface Organization {
  id: string;
  name: string;
  slug: string;
  role: 'owner' | 'admin' | 'member' | 'viewer';
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  currentOrganizationId: string | null;
  organizations: Organization[];
  isAuthenticated: boolean;
  isLoading: boolean;
  
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  setCurrentOrganization: (orgId: string) => void;
}

interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  organizationName?: string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      currentOrganizationId: null,
      organizations: [],
      isAuthenticated: false,
      isLoading: false,
      
      login: async (email, password) => {
        set({ isLoading: true });
        
        try {
          const response = await api.post('/auth/login/', { email, password });
          const { user, access_token, refresh_token, organizations } = response.data;
          
          set({
            user,
            accessToken: access_token,
            refreshToken: refresh_token,
            organizations,
            currentOrganizationId: organizations[0]?.id || null,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },
      
      register: async (data) => {
        set({ isLoading: true });
        
        try {
          const response = await api.post('/auth/register/', data);
          const { user, access_token, refresh_token, organization } = response.data;
          
          set({
            user,
            accessToken: access_token,
            refreshToken: refresh_token,
            organizations: organization ? [organization] : [],
            currentOrganizationId: organization?.id || null,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },
      
      logout: () => {
        api.post('/auth/logout/').catch(() => {});
        
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          currentOrganizationId: null,
          organizations: [],
          isAuthenticated: false,
        });
      },
      
      refreshToken: async () => {
        const currentRefreshToken = get().refreshToken;
        
        if (!currentRefreshToken) {
          throw new Error('No refresh token');
        }
        
        const response = await api.post('/auth/token/refresh/', {
          refresh: currentRefreshToken,
        });
        
        set({
          accessToken: response.data.access,
          refreshToken: response.data.refresh,
        });
      },
      
      setCurrentOrganization: (orgId) => {
        set({ currentOrganizationId: orgId });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        currentOrganizationId: state.currentOrganizationId,
        organizations: state.organizations,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
6.4 Singapore Formatting Utilities
TypeScript

// lib/utils/singapore.ts
/**
 * Singapore-specific formatting utilities
 */

import { format, formatDistance } from 'date-fns';

/**
 * Format currency in SGD
 */
export function formatSGD(amount: number): string {
  return new Intl.NumberFormat('en-SG', {
    style: 'currency',
    currency: 'SGD',
    minimumFractionDigits: 2,
  }).format(amount);
}

/**
 * Format cents to SGD
 */
export function formatCentsToSGD(cents: number): string {
  return formatSGD(cents / 100);
}

/**
 * Format Singapore phone number
 */
export function formatSGPhone(phone: string): string {
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length === 8 && /^[89]/.test(cleaned)) {
    return `+65 ${cleaned.slice(0, 4)} ${cleaned.slice(4)}`;
  }
  
  if (cleaned.startsWith('65') && cleaned.length === 10) {
    return `+65 ${cleaned.slice(2, 6)} ${cleaned.slice(6)}`;
  }
  
  return phone;
}

/**
 * Validate Singapore UEN
 */
export function isValidUEN(uen: string): boolean {
  if (!uen) return false;
  
  const patterns = [
    /^[0-9]{8}[A-Z]$/,       // Local company
    /^[0-9]{9}[A-Z]$/,       // Business
    /^[TSRF][0-9]{2}[A-Z]{2}[0-9]{4}[A-Z]$/,  // Foreign/Others
  ];
  
  return patterns.some((pattern) => pattern.test(uen.toUpperCase()));
}

/**
 * Format date for Singapore (DD MMM YYYY)
 */
export function formatSGDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return format(d, 'dd MMM yyyy');
}

/**
 * Format datetime for Singapore
 */
export function formatSGDateTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return format(d, 'dd MMM yyyy, HH:mm');
}

/**
 * Relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return formatDistance(d, new Date(), { addSuffix: true });
}

/**
 * Calculate GST (9%)
 */
export function calculateGST(amountCents: number): {
  subtotal: number;
  gst: number;
  total: number;
} {
  const gstRate = 0.09;
  const subtotal = amountCents;
  const gst = Math.round(subtotal * gstRate);
  const total = subtotal + gst;
  
  return { subtotal, gst, total };
}

/**
 * Singapore public holidays 2026 (update annually)
 */
export const SG_HOLIDAYS_2026 = [
  { date: '2026-01-01', name: "New Year's Day" },
  { date: '2026-01-29', name: 'Chinese New Year' },
  { date: '2026-01-30', name: 'Chinese New Year' },
  { date: '2026-04-03', name: 'Good Friday' },
  { date: '2026-05-01', name: 'Labour Day' },
  { date: '2026-05-12', name: 'Vesak Day' },
  { date: '2026-06-07', name: 'Hari Raya Haji' },
  { date: 
