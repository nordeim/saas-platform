# Project Requirements Document (PRD)

## Project Name: NexusCore — English-Only SaaS Corporate Website & Marketing Platform (Pragmatic Production Release)
**Version:** 2.0 (merged, pragmatic, English-only)  
**Date:** December 22, 2025  
**Primary Stack:**  
- **Backend:** Django 6.0 + Django REST Framework (DRF) + Celery + django-tasks  
- **Frontend:** Next.js 14.2+ (App Router) + React 18 + TypeScript  
- **DB / Cache:** PostgreSQL 16+, Redis 7.4+  
- **Python:** 3.12+  
- **Hosting/Infra:** Containerized (Docker) → Cloud (managed K8s or managed App Service) + CDN (Cloudflare/AWS CloudFront)  
- **Primary PSP:** Stripe (SGD pricing with PayNow via Stripe where supported)

---

## 1. Executive Summary

Build a production-ready, English-only marketing & lead-management site for a Singapore-based medium B2B SaaS company. This is a complete drop-in replacement PRD that merges strategic market context, design guidance, and concrete engineering deliverables into a pragmatic, implementable plan. The MVP focuses on marketing pages, lead capture, trial onboarding, subscription billing, and an admin for operations. Accessibility (WCAG AA), performance (pragmatic Core Web Vitals), security, and PDPA-compliant data handling are non-negotiable.

**Primary goals:**
- Convert visitors → qualified leads → trials/demos with measurable funnels
- Provide robust subscription and invoice flows with production-grade webhook and retry handling
- Ship within a practical phased delivery (MVP in 10–12 weeks with phased enhancements)
- Maintainable, secure, and testable architecture for rapid iteration

---

## 2. Core Goals & Success Metrics

### Business Goals
- Generate qualified leads and reduce friction to trial/demo
- Provide marketing & sales with measurable funnel events
- Run a reliable billing/trial pipeline for revenue capture
- Meet Singapore PDPA requirements for consent and DSARs

### Success Metrics (90-day targets post-launch)
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Trial/Demo signups | +30% over baseline | GA4 conversion tracking |
| Visitor → CTA click conversion | ≥ 5% on pricing pages | Heatmaps + event tracking |
| Mobile LCP (launch) | ≤ 2.5s → ≤ 2.0s within 60 days | Lighthouse + RUM |
| WCAG AA compliance | No critical failures for primary flows | axe-core + manual audit |
| Payment webhook success | ≥ 99.9% processing success | Stripe logs + monitoring |
| DSAR fulfillment SLA | ≤ 72 hours for export requests | DSAR workflow tracking |

---

## 3. Scope Definition

### MVP (In-Scope)
**Marketing Pages:**
- Home, Product/Solutions, Pricing, Case Studies, Resources (blog), Contact, Privacy/Terms, FAQ
- Lead capture forms (UTM capture), demo-request flow, newsletter sign-up

**User Authentication:**
- Email signup, verify, password reset, simple trial onboarding
- Session management with secure cookies

**Subscription & Billing:**
- Stripe integration (trial, starter, pro plans)
- Invoice generation and PDF downloads
- Webhook processing + Celery background tasks
- Dunning strategy for failed payments

**Admin Dashboard:**
- Django admin + lightweight custom admin pages
- Users, leads, subscriptions, invoices management
- CSV exports and audit logs

**Operational Infrastructure:**
- Background jobs (Celery + Redis)
- DSAR endpoints and workflows
- Monitoring and alerting (Sentry, Prometheus)
- CI/CD pipelines and deployment automation

**Compliance:**
- PDPA-compliant data handling
- Cookie consent management
- DSAR endpoints (`/api/v1/dsar/export/`, `/api/v1/dsar/delete/`)
- Data retention policies

### Out of Scope (MVP)
- Full ERP-level accounting/inventory modules (only demo mockups in MVP)
- Enterprise SSO beyond OAuth/SAML basics
- Multi-language support (English-only initial)
- Advanced CRM two-way sync (basic outbound webhooks in MVP)
- Mobile app development
- AI-powered features

---

## 4. Technical Architecture

### High-Level Architecture Diagram
```
[User Browser] → Next.js (SSG/SSR) → DRF API (HTTPS) → Django Business Logic
       │                │                 │
       │                │                 ├── PostgreSQL 16 (Primary DB)
       │                │                 ├── Redis 7.4 (Cache/Broker)
       │                │                 └── Celery Workers (Background Jobs)
       │                │
       │                └── CDN (Static Assets)
       │
       └── Third-party Services:
           ├── Stripe (Payments)
           ├── SendGrid/SES (Email)
           ├── CRM (Lead webhooks)
           └── Sentry (Error Monitoring)
```

### Technology Stack Justification

**Why Django 6.0 + Next.js 14?**
- **Django 6.0:** Battle-tested ORM with excellent PostgreSQL support, built-in admin panel, robust security features, mature ecosystem, async support, and strong community in Singapore
- **Next.js 14:** Hybrid rendering (SSG/SSR/ISR) for optimal performance, excellent TypeScript support, built-in API routes, Vercel deployment optimization, active community
- **Combined Benefits:** Clear separation of concerns, best-in-class performance for both marketing and application needs, scalable architecture, available talent pool

**Why PostgreSQL 16 + Redis 7.4?**
- **PostgreSQL 16:** JSONB support for flexible data structures, excellent performance for complex queries, strong ACID compliance for financial data, cost-effective
- **Redis 7.4:** Blazing fast performance for caching and sessions, built-in data structures for complex operations, excellent Celery integration, cluster support for high availability

### Django 6.0 Specific Implementation Details
```python
# Django 6.0 settings.py highlights
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c statement_timeout=5000',  # 5 second timeout
            'application_name': 'nexuscore'
        }
    }
}

# Django 6.0 async support for background tasks
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # For reliable task processing

# Django 6.0 security enhancements
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Django 6.0 performance optimizations
CONN_MAX_AGE = 60  # Persistent database connections
CONN_HEALTH_CHECKS = True  # Django 6.0+ health checks

# Django 6.0 cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        }
    }
}
```

---

## 5. User Journeys & Event Taxonomy

### Core User Journeys

**Journey 1: Visitor → Trial User**
1. Lands on homepage → explores features → views pricing
2. Clicks "Start Free Trial" → completes signup form
3. Receives email verification → verifies account
4. Completes trial onboarding → accesses demo dashboard
5. Uses demo features → evaluates conversion to paid plan

**Journey 2: Visitor → Demo Request**
1. Views case studies → clicks "Request Demo"
2. Completes demo request form with business context
3. System creates CRM lead with UTM data
4. Sales team notified → schedules demo call
5. Follow-up workflow initiated

**Journey 3: Trial User → Paid Customer**
1. Navigates to pricing/upgrade page
2. Selects plan → enters payment details via Stripe
3. System processes payment → activates subscription
4. Receives invoice email → accesses full features
5. Uses product → potentially upgrades plan later

### Event Taxonomy & Acceptance Matrix

| Flow | Event Name | Key Properties | Success Criteria / Acceptance Test |
|------|------------|----------------|-----------------------------------|
| Visitor page view | `page_view` | `page`, `url`, `utm_source`, `device` | Event recorded server-side/GA4 on every page view; sample export available |
| Hero CTA click | `cta_click` | `cta_id`, `page`, `user_id?` | Click recorded; UI shows expected modal/redirect |
| Demo request | `demo_request_submitted` | `lead_id`, `email`, `utm` | Lead saved in DB; webhook to CRM fired; sales notified |
| Trial signup | `trial_started` | `user_id`, `org_id`, `plan_id` | User created, trial flag set, confirmation email queued & sent |
| Subscription created | `subscription_created` | `subscription_id`, `stripe_id`, `amount` | Subscription active after Stripe webhook; invoice generated |
| Invoice paid | `invoice_paid` | `invoice_id`, `amount`, `stripe_invoice_id` | Celery webhook processed idempotently; invoice status updated |
| DSAR export requested | `dsar_request` | `user_id`, `request_id` | DSAR package created within SLA (≤72 hours) and link/email sent |
| Payment failure | `payment_failed` | `subscription_id`, `reason` | Dunning tasks start; notifications sent; monitoring alert triggered |

**Acceptance Matrix Example for `subscription_created`:**
- POST `/api/v1/subscriptions/` with card token → DRF returns 201 and `subscription_id`
- Stripe creates subscription → Stripe webhook `invoice.payment_succeeded` received
- Webhook processed by Celery `process_stripe_webhook` task, idempotency key used
- DB subscription becomes `active`
- Invoice PDF generated and uploaded to S3
- Notification email sent
- End-to-end E2E test passes

---

## 6. API Surface (Pragmatic & Concrete)

All endpoints under `/api/v1/` with HTTPS and JSON. Authentication via JWT tokens.

### Auth Endpoints
```http
POST /api/v1/auth/register/          { email, password, company_name, plan_id? } -> 201
POST /api/v1/auth/login/             { email, password } -> session cookie or tokens
POST /api/v1/auth/logout/
POST /api/v1/auth/verify-email/      { token }
POST /api/v1/auth/password-reset/    { token, new_password }
```

### Leads & Contact
```http
POST /api/v1/leads/                  { name, email, company, role, utm... } -> lead_id
GET  /api/v1/leads/?status=new       (admin)
POST /api/v1/leads/{id}/assign/      { owner_id }
POST /api/v1/demo-request/           { name, email, company, preferred_time, timezone, utm_* }
```

### Subscriptions & Billing
```http
GET  /api/v1/plans/
POST /api/v1/subscriptions/          { org_id, plan_id, payment_method_id }
GET  /api/v1/subscriptions/{id}/
POST /api/v1/subscriptions/{id}/cancel/
POST /api/v1/subscriptions/{id}/change-plan/ { plan_id }
GET  /api/v1/invoices/
GET  /api/v1/invoices/{id}/download/  (PDF)
```

### Webhooks
```http
POST /api/v1/webhooks/stripe/        (verify signature, enqueue)
```

### DSAR & Privacy
```http
POST /api/v1/dsar/export/            { user_email } -> request_id
POST /api/v1/dsar/delete/            { user_email } -> request_id
GET  /api/v1/dsar/status/{id}/
```

### Django 6.0 API Implementation Example
```python
# views.py - SubscriptionViewSet using Django 6.0 async support
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from celery.result import AsyncResult

class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Django 6.0 optimized SubscriptionViewSet with async task handling
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(
            organization__members=self.request.user
        ).select_related('organization', 'plan')
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create subscription with idempotency key handling
        """
        idempotency_key = request.headers.get('Idempotency-Key')
        if not idempotency_key:
            return Response(
                {'error': 'Idempotency-Key header required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for existing request with same idempotency key
        existing = IdempotencyRecord.objects.filter(
            key=idempotency_key,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).first()
        
        if existing:
            if existing.status == 'completed':
                return Response(existing.response_data, status=status.HTTP_201_CREATED)
            elif existing.status == 'processing':
                return Response(
                    {'status': 'processing'},
                    status=status.HTTP_202_ACCEPTED
                )
        
        # Create new idempotency record
        record = IdempotencyRecord.objects.create(
            key=idempotency_key,
            request_data=request.data,
            status='processing'
        )
        
        try:
            # Process subscription creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            # Enqueue async Stripe processing
            task = process_stripe_subscription.delay(
                subscription_id=serializer.instance.id,
                payment_method_id=request.data.get('payment_method_id')
            )
            
            # Update idempotency record
            record.task_id = task.id
            record.status = 'processing'
            record.save()
            
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            record.status = 'failed'
            record.error = str(e)
            record.save()
            raise
    
    @action(detail=True, methods=['post'])
    async def cancel(self, request, pk=None):
        """
        Django 6.0 async cancellation endpoint
        """
        subscription = await self.aget_object()
        if subscription.status == 'cancelled':
            return Response({'detail': 'Already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Async cancellation with Celery
        cancellation_task = cancel_subscription_task.delay(
            subscription_id=subscription.id,
            reason=request.data.get('reason', 'user_requested')
        )
        
        return Response({
            'status': 'cancellation_initiated',
            'task_id': cancellation_task.id
        }, status=status.HTTP_202_ACCEPTED)
```

---

## 7. Data Model (Core Entities)

### PostgreSQL 16 Schema (Django 6.0 Models)
```python
from django.db import models
from django.contrib.postgres.fields import JSONField

class User(models.Model):
    """Django 6.0 custom user model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('user', 'User'),
        ('viewer', 'Viewer')
    ], default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]

class Organization(models.Model):
    """Company/organization entity"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    billing_contact = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    timezone = models.CharField(max_length=50, default='Asia/Singapore')
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['stripe_customer_id']),
        ]

class Plan(models.Model):
    """Subscription plan definitions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)  # 'Starter', 'Professional', 'Enterprise'
    sku = models.CharField(max_length=50, unique=True)  # 'starter-monthly', 'pro-annual'
    price_monthly_cents = models.IntegerField()
    price_annual_cents = models.IntegerField()
    features = JSONField(default=dict)  # Feature flags and limits
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['is_active']),
        ]

class Subscription(models.Model):
    """Customer subscription state"""
    STATUS_CHOICES = [
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('cancelled', 'Cancelled'),
        ('unpaid', 'Unpaid'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['status', 'current_period_end']),
            models.Index(fields=['stripe_subscription_id']),
        ]

class Invoice(models.Model):
    """Billing invoices"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('uncollectible', 'Uncollectible'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name='invoices')
    amount_cents = models.IntegerField()
    currency = models.CharField(max_length=3, default='SGD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    pdf_url = models.URLField(blank=True)
    stripe_invoice_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    
    class Meta:
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['status', 'due_date']),
            models.Index(fields=['stripe_invoice_id']),
        ]

class Lead(models.Model):
    """Marketing leads"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('disqualified', 'Disqualified'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255)
    source = models.CharField(max_length=50)  # 'organic', 'paid', 'referral'
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    owner_id = models.UUIDField(null=True, blank=True)  # User ID who owns this lead
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['email']),
        ]

class DSARRequest(models.Model):
    """Data Subject Access Request tracking"""
    REQUEST_TYPE_CHOICES = [
        ('export', 'Data Export'),
        ('delete', 'Data Deletion'),
        ('access', 'Data Access'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_email = models.EmailField()
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    export_url = models.URLField(blank=True)  # S3 URL for exported data
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'requested_at']),
            models.Index(fields=['user_email']),
        ]
```

### Indexing Strategy
```sql
-- Critical indexes for performance optimization
CREATE INDEX CONCURRENTLY idx_subscriptions_active_org ON subscriptions(organization_id) 
WHERE status = 'active';

CREATE INDEX CONCURRENTLY idx_invoices_paid_recent ON invoices(organization_id, created_at) 
WHERE status = 'paid' AND created_at >= NOW() - INTERVAL '3 months';

CREATE INDEX CONCURRENTLY idx_leads_new_status ON leads(status) 
WHERE status = 'new';

CREATE INDEX CONCURRENTLY idx_dsar_pending ON dsar_requests(status) 
WHERE status = 'pending';

-- Full-text search indexes for admin queries
CREATE INDEX CONCURRENTLY idx_organizations_search ON organizations 
USING gin(to_tsvector('english', name));

CREATE INDEX CONCURRENTLY idx_leads_search ON leads 
USING gin(to_tsvector('english', name || ' ' || company || ' ' || email));
```

---

## 8. Background Jobs & Celery Tasks

### Queue Priorities
- **high**: webhook processing, billing actions, DSAR processing
- **default**: transactional emails, invoice generation, lead processing  
- **low**: reports, exports, cleanup tasks

### Critical Celery Tasks (Django 6.0 + Celery 5.x)
```python
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.db import transaction
from django.conf import settings
import stripe
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, retry_backoff=True, retry_backoff_max=600)
def process_stripe_webhook(self, payload, signature):
    """
    Process Stripe webhooks with idempotency and retry handling
    """
    try:
        # Verify signature
        stripe.WebhookSignature.verify_header(
            payload, signature, settings.STRIPE_WEBHOOK_SECRET
        )
        
        event = stripe.Event.construct_from(payload, settings.STRIPE_API_VERSION)
        event_id = event.id
        
        # Check for duplicate processing
        if WebhookEvent.objects.filter(event_id=event_id).exists():
            logger.info(f"Duplicate webhook event {event_id} - skipping")
            return {'status': 'duplicate'}
        
        with transaction.atomic():
            # Record event processing
            webhook_event = WebhookEvent.objects.create(
                event_id=event_id,
                event_type=event.type,
                data=event.data,
                processed=False
            )
            
            # Route to specific handlers
            if event.type == 'invoice.payment_succeeded':
                handle_invoice_payment(event)
            elif event.type == 'customer.subscription.updated':
                handle_subscription_update(event)
            elif event.type == 'customer.subscription.deleted':
                handle_subscription_cancellation(event)
            elif event.type == 'payment_intent.payment_failed':
                handle_payment_failure(event)
            
            # Mark as processed
            webhook_event.processed = True
            webhook_event.save()
            
        logger.info(f"Successfully processed webhook event {event_id}")
        return {'status': 'success', 'event_id': event_id}
        
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid Stripe signature: {str(e)}")
        raise self.retry(exc=e)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        try:
            self.retry(exc=e)
        except MaxRetriesExceededError:
            logger.critical(f"Max retries exceeded for webhook processing: {str(e)}")
            # Alert engineering team
            send_alert_to_engineering(
                "Webhook processing failed after max retries",
                f"Event payload: {payload[:500]}..."
            )
            raise

@shared_task(bind=True, max_retries=3)
def generate_invoice_pdf(self, invoice_id):
    """
    Generate PDF invoice and upload to S3
    """
    from invoices.models import Invoice
    from invoices.utils import render_invoice_pdf
    
    try:
        invoice = Invoice.objects.select_related('organization').get(id=invoice_id)
        
        # Generate PDF
        pdf_content = render_invoice_pdf(invoice)
        
        # Upload to S3
        s3_key = f"invoices/{invoice.organization_id}/{invoice.id}.pdf"
        s3_url = upload_to_s3(pdf_content, s3_key, content_type='application/pdf')
        
        # Update invoice record
        invoice.pdf_url = s3_url
        invoice.save()
        
        logger.info(f"Generated PDF for invoice {invoice_id}")
        return {'status': 'success', 'pdf_url': s3_url}
        
    except Invoice.DoesNotExist:
        logger.error(f"Invoice {invoice_id} does not exist")
        return {'status': 'error', 'message': 'Invoice not found'}
    except Exception as e:
        logger.error(f"Error generating invoice PDF: {str(e)}")
        self.retry(exc=e)

@shared_task
def process_dsar_export(dsar_id):
    """
    Process DSAR export request - compile user data into export package
    """
    from privacy.models import DSARRequest
    from privacy.utils import compile_user_data_export
    
    try:
        dsar = DSARRequest.objects.get(id=dsar_id, request_type='export')
        
        if dsar.status != 'pending':
            logger.info(f"DSAR {dsar_id} already processed - status: {dsar.status}")
            return
        
        dsar.status = 'processing'
        dsar.save()
        
        # Compile user data export
        export_data = compile_user_data_export(dsar.user_email)
        
        # Create ZIP archive and upload to S3
        zip_content = create_zip_archive(export_data)
        s3_key = f"dsar_exports/{dsar.id}_{dsar.user_email.replace('@', '_')}.zip"
        export_url = upload_to_s3(zip_content, s3_key, content_type='application/zip')
        
        # Update DSAR record
        dsar.export_url = export_url
        dsar.status = 'completed'
        dsar.processed_at = timezone.now()
        dsar.save()
        
        # Notify user and admin
        send_dsar_completion_email(dsar.user_email, export_url)
        send_dsar_notification_to_admin(dsar)
        
        logger.info(f"Completed DSAR export for {dsar.user_email}")
        return {'status': 'completed', 'export_url': export_url}
        
    except DSARRequest.DoesNotExist:
        logger.error(f"DSAR request {dsar_id} not found")
        return {'status': 'error', 'message': 'DSAR not found'}
    except Exception as e:
        logger.error(f"Error processing DSAR export: {str(e)}")
        if hasattr(dsar, 'id'):
            dsar.status = 'failed'
            dsar.failure_reason = str(e)
            dsar.save()
        raise
```

### Task Monitoring & Alerting
```python
# Celery monitoring with Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

celery_tasks_total = Counter('celery_tasks_total', 'Total celery tasks', ['task_name', 'status'])
celery_task_duration = Histogram('celery_task_duration_seconds', 'Celery task duration', ['task_name'])
celery_queue_length = Gauge('celery_queue_length', 'Number of tasks in queue', ['queue_name'])

@app.task(base=LoggingTask)
def monitored_task(*args, **kwargs):
    """Base task class with monitoring"""
    task_name = self.name
    start_time = time.time()
    
    try:
        celery_tasks_total.labels(task_name=task_name, status='started').inc()
        result = self.run(*args, **kwargs)
        duration = time.time() - start_time
        celery_task_duration.labels(task_name=task_name).observe(duration)
        celery_tasks_total.labels(task_name=task_name, status='success').inc()
        return result
    except Exception as e:
        duration = time.time() - start_time
        celery_task_duration.labels(task_name=task_name).observe(duration)
        celery_tasks_total.labels(task_name=task_name, status='failed').inc()
        logger.error(f"Task {task_name} failed: {str(e)}")
        raise
```

---

## 9. Design System & UX Requirements

### Design Principles (Pragmatic)
- **Performance-first:** Small bundle sizes, critical CSS, defer non-critical scripts
- **Accessibility-first:** Semantic HTML, keyboard navigation, visible focus states
- **Clarity & conversion:** Concise hero, pricing clarity, minimal form friction
- **Maintainability:** Reusable components, consistent design tokens, documented patterns

### Visual Design System (Practical)
```css
/* Core design tokens - tailwind.config.js */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6f1ff',
          100: '#cce3ff',
          200: '#99caff',
          300: '#66b1ff',
          400: '#3399ff',
          500: '#007bff',    // Primary brand blue
          600: '#0066cc',
          700: '#0052a3',
          800: '#003d7a',
          900: '#002952'
        },
        success: {
          500: '#28a745'    // Green for success states
        },
        warning: {
          500: '#ffc107'    // Yellow for warnings
        },
        danger: {
          500: '#dc3545'    // Red for errors/critical actions
        }
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      spacing: {
        '0': '0',
        '1': '0.25rem',   // 4px
        '2': '0.5rem',    // 8px
        '3': '0.75rem',   // 12px
        '4': '1rem',      // 16px
        '5': '1.25rem',   // 20px
        '6': '1.5rem',    // 24px
        '8': '2rem',      // 32px
        '10': '2.5rem',   // 40px
        '12': '3rem',     // 48px
      }
    }
  }
}
```

### Core Components (Accessible & Performant)
```jsx
// PricingCard.jsx - Accessible pricing component
import { useState, useEffect } from 'react';
import { Button } from './Button';
import { CheckCircleIcon } from '@heroicons/react/24/solid';

export function PricingCard({ plan, onSelect, isMostPopular = false }) {
  const [isAnnual, setIsAnnual] = useState(false);
  
  // Annual pricing calculation
  const price = isAnnual ? plan.price_annual : plan.price_monthly;
  const savings = plan.price_monthly * 12 - plan.price_annual;
  
  return (
    <div 
      className={`relative rounded-2xl border-2 ${isMostPopular ? 'border-primary-500' : 'border-gray-200'}`}
      role="region"
      aria-labelledby={`plan-${plan.id}-title`}
    >
      {isMostPopular && (
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
          <span className="bg-primary-500 text-white px-3 py-1 rounded-full text-sm font-medium">
            Most Popular
          </span>
        </div>
      )}
      
      <div className="p-6">
        <h3 
          id={`plan-${plan.id}-title`}
          className="text-xl font-bold text-gray-900"
        >
          {plan.name}
        </h3>
        
        <div className="mt-4 flex items-baseline">
          <span className="text-4xl font-bold text-gray-900">SGD {price}</span>
          <span className="ml-1 text-gray-500">/{isAnnual ? 'year' : 'month'}</span>
        </div>
        
        {isAnnual && savings > 0 && (
          <p className="mt-1 text-sm text-primary-600">
            Save SGD {savings} compared to monthly billing
          </p>
        )}
        
        <div className="mt-6">
          <Button
            fullWidth
            onClick={() => onSelect(plan)}
            aria-label={`Select ${plan.name} plan`}
          >
            Get Started
          </Button>
        </div>
        
        <ul className="mt-6 space-y-3" role="list">
          {plan.features.map((feature, index) => (
            <li key={index} className="flex items-start">
              <CheckCircleIcon className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" aria-hidden="true" />
              <span className="ml-3 text-gray-700">{feature}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// DSARForm.jsx - Accessible DSAR request form
export function DSARForm() {
  const [email, setEmail] = useState('');
  const [requestType, setRequestType] = useState('export');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    
    try {
      const response = await fetch('/api/v1/dsar/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, request_type: requestType }),
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to submit request');
      }
      
      setSuccess(true);
      setEmail('');
      
      // Reset form after 5 seconds
      setTimeout(() => {
        setSuccess(false);
      }, 5000);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-2">Data Privacy Request</h2>
      <p className="text-gray-600 mb-6">
        Submit a request to access, export, or delete your personal data in accordance with PDPA.
      </p>
      
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md" role="alert">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-md" role="status">
          Your request has been submitted successfully. We will process it within 72 hours.
        </div>
      )}
      
      <form onSubmit={handleSubmit} noValidate>
        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email Address
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            aria-describedby="email-helper"
          />
          <p id="email-helper" className="mt-1 text-xs text-gray-500">
            The email address associated with your account
          </p>
        </div>
        
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Request Type
          </label>
          <div className="space-y-2">
            {[
              { value: 'export', label: 'Export my data' },
              { value: 'delete', label: 'Delete my data' },
              { value: 'access', label: 'Access my data' }
            ].map((option) => (
              <div key={option.value} className="flex items-center">
                <input
                  id={`request-${option.value}`}
                  type="radio"
                  name="requestType"
                  value={option.value}
                  checked={requestType === option.value}
                  onChange={(e) => setRequestType(e.target.value)}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500"
                  aria-describedby={`request-${option.value}-desc`}
                />
                <label 
                  htmlFor={`request-${option.value}`} 
                  className="ml-3 text-sm font-medium text-gray-700"
                >
                  {option.label}
                </label>
                <p id={`request-${option.value}-desc`} className="ml-6 text-xs text-gray-500">
                  {option.value === 'export' ? 'Receive a copy of your data' : 
                   option.value === 'delete' ? 'Permanently remove your data' : 
                   'View your stored personal information'}
                </p>
              </div>
            ))}
          </div>
        </div>
        
        <p className="text-xs text-gray-500 mb-4">
          By submitting this request, you acknowledge that we will process it within 72 hours as required by PDPA regulations.
        </p>
        
        <button
          type="submit"
          disabled={isSubmitting}
          className={`w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
            isSubmitting ? 'opacity-75 cursor-not-allowed' : ''
          }`}
        >
          {isSubmitting ? 'Submitting...' : 'Submit Request'}
        </button>
      </form>
      
      <div className="mt-6 pt-6 border-t border-gray-200">
        <p className="text-sm text-gray-600">
          For urgent requests or questions, contact our Data Protection Officer at{' '}
          <a href="mailto:dpo@company.com" className="text-primary-600 hover:text-primary-700">
            dpo@company.com
          </a>
        </p>
      </div>
    </div>
  );
}
```

### Performance & Accessibility Requirements
- **Mobile LCP (launch):** ≤ 2.5s → ≤ 2.0s within 60 days
- **WCAG AA compliance:** No critical failures for primary flows (signup, checkout, pricing)
- **Critical CSS:** Inline critical CSS for above-the-fold content
- **Image optimization:** Use AVIF/WebP formats with srcset and lazy loading
- **Third-party script governance:** Load analytics/marketing scripts via GTM server-side or asynchronously
- **Keyboard navigation:** All interactive elements accessible via keyboard
- **Screen reader testing:** Manual testing with NVDA/VoiceOver for primary flows

---

## 10. Security & Compliance (PDPA-Focused)

### Application Security (Django 6.0 Hardening)
```python
# settings.py - Security hardening for Django 6.0
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", 'https://*.stripe.com', 'https://www.googletagmanager.com')
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", 'data:', 'https://*.cloudfront.net')
CSP_CONNECT_SRC = ("'self'", 'https://*.stripe.com', 'https://api.sendgrid.com')
CSP_FONT_SRC = ("'self'", 'data:')
CSP_FRAME_SRC = ("'self'", 'https://*.stripe.com')
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)

# Rate limiting for authentication endpoints
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'login': '5/minute',
        'password_reset': '3/hour'
    }
}
```

### PDPA Compliance Implementation
```python
# privacy/views.py - DSAR endpoints
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.conf import settings
import boto3
import json
import logging

logger = logging.getLogger(__name__)

class DSARSubmitView(APIView):
    """
    Handle DSAR submission requests
    """
    def post(self, request):
        email = request.data.get('email')
        request_type = request.data.get('request_type', 'export')
        
        if not email:
            return Response(
                {'error': 'Email address is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request_type not in ['export', 'delete', 'access']:
            return Response(
                {'error': 'Invalid request type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create DSAR record
        dsar = DSARRequest.objects.create(
            user_email=email,
            request_type=request_type,
            status='pending'
        )
        
        # Queue processing task
        if request_type == 'export':
            process_dsar_export.delay(dsar.id)
        elif request_type == 'delete':
            process_dsar_deletion.delay(dsar.id)
        elif request_type == 'access':
            process_dsar_access.delay(dsar.id)
        
        logger.info(f"DSAR submitted for {email} - type: {request_type}")
        
        return Response({
            'dsar_id': dsar.id,
            'status': 'pending',
            'estimated_completion': '72 hours'
        }, status=status.HTTP_202_ACCEPTED)

class DSARStatusView(APIView):
    """
    Check DSAR processing status
    """
    def get(self, request, dsar_id):
        try:
            dsar = DSARRequest.objects.get(id=dsar_id)
        except DSARRequest.DoesNotExist:
            return Response(
                {'error': 'DSAR not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        response_data = {
            'dsar_id': dsar.id,
            'status': dsar.status,
            'request_type': dsar.request_type,
            'created_at': dsar.requested_at,
            'processed_at': dsar.processed_at,
        }
        
        if dsar.status == 'completed' and dsar.export_url:
            response_data['export_url'] = dsar.export_url
        
        return Response(response_data)
```

### Data Retention & Deletion Policy
- **User accounts:** 24 months after account deletion
- **Billing data:** 7 years for tax compliance
- **Lead data:** 12 months after last interaction
- **Logs:** 90 days for operational debugging, 2 years for security audits
- **DSAR exports:** 30 days after generation, then automatically deleted

### Penetration Testing Requirements
- **Pre-launch:** External pen test by certified vendor focusing on auth, payments, and data leakage
- **Quarterly:** Automated vulnerability scanning with OWASP ZAP or similar
- **Annual:** Full security audit including infrastructure and application layers
- **Critical findings:** SLA of 48 hours for remediation

---

## 11. Testing Strategy & Quality Assurance

### Testing Pyramid (Pragmatic Coverage Targets)
```python
# Backend tests - pytest with factory_boy
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from factories import UserFactory, OrganizationFactory, PlanFactory, SubscriptionFactory

@pytest.mark.django_db
class TestSubscriptionAPI:
    """Comprehensive subscription API testing"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.organization = OrganizationFactory(owner=self.user)
        self.plan = PlanFactory(price_monthly_cents=1500, price_annual_cents=15000)
        self.client.force_authenticate(user=self.user)
    
    def test_create_subscription_with_idempotency(self):
        """Test subscription creation with idempotency key"""
        url = reverse('api:subscriptions-list')
        headers = {'Idempotency-Key': 'test-key-123'}
        data = {
            'organization_id': str(self.organization.id),
            'plan_id': str(self.plan.id),
            'payment_method_id': 'pm_test_123'
        }
        
        # First request
        response1 = self.client.post(url, data, headers=headers)
        assert response1.status_code == status.HTTP_201_CREATED
        subscription_id = response1.data['id']
        
        # Second request with same idempotency key
        response2 = self.client.post(url, data, headers=headers)
        assert response2.status_code == status.HTTP_201_CREATED
        assert response2.data['id'] == subscription_id
    
    def test_webhook_processing_idempotency(self):
        """Test webhook processing with duplicate events"""
        webhook_url = reverse('api:webhooks-stripe')
        payload = {
            'id': 'evt_test_duplicate',
            'type': 'invoice.payment_succeeded',
            'data': {'object': {'id': 'inv_test_123'}}
        }
        signature = 'test_signature'
        
        # First webhook
        response1 = self.client.post(
            webhook_url, 
            data=json.dumps(payload), 
            content_type='application/json',
            headers={'Stripe-Signature': signature}
        )
        assert response1.status_code == status.HTTP_200_OK
        
        # Second webhook (duplicate)
        response2 = self.client.post(
            webhook_url, 
            data=json.dumps(payload), 
            content_type='application/json',
            headers={'Stripe-Signature': signature}
        )
        assert response2.status_code == status.HTTP_200_OK
        assert response2.data['status'] == 'duplicate'

# Frontend tests - Cypress E2E
describe('Subscription Flow', () => {
  beforeEach(() => {
    cy.loginAsTestUser();
    cy.intercept('POST', '/api/v1/subscriptions/', { fixture: 'subscription-response.json' }).as('createSubscription');
    cy.intercept('POST', '/api/v1/webhooks/stripe/', { success: true }).as('processWebhook');
  });

  it('completes end-to-end subscription flow', () => {
    // Navigate to pricing page
    cy.visit('/pricing');
    
    // Select professional plan
    cy.get('[data-testid="pricing-card-professional"]').within(() => {
      cy.get('button').contains('Get Started').click();
    });
    
    // Fill payment details (mock Stripe)
    cy.get('#card-element').type('4242424242424242{enter}12{enter}25{enter}123');
    
    // Submit subscription
    cy.get('form').submit();
    cy.wait('@createSubscription');
    
    // Verify success message
    cy.contains('Subscription created successfully');
    cy.contains('Your invoice has been emailed to you');
    
    // Check webhook processing
    cy.wait('@processWebhook');
    
    // Verify subscription status
    cy.visit('/account/billing');
    cy.contains('Active');
    cy.contains('Professional Plan');
  });

  it('handles payment failure gracefully', () => {
    // Mock payment failure
    cy.intercept('POST', '/api/v1/subscriptions/', {
      statusCode: 402,
      body: { error: 'Your card was declined' }
    }).as('failedSubscription');
    
    cy.visit('/pricing');
    cy.get('[data-testid="pricing-card-starter"]').within(() => {
      cy.get('button').contains('Get Started').click();
    });
    
    cy.get('#card-element').type('4000000000000002{enter}12{enter}25{enter}123');
    cy.get('form').submit();
    cy.wait('@failedSubscription');
    
    // Verify error handling
    cy.contains('Payment failed');
    cy.contains('Your card was declined');
    cy.get('button').contains('Try Again').should('be.visible');
  });
});
```

### Quality Gates
- **Pre-merge:** All unit tests pass, security scans clean, linting checks pass
- **Pre-production:** E2E tests pass in staging, Lighthouse performance ≥ 60, accessibility score ≥ 90
- **Post-launch:** Real user monitoring active, error tracking below 0.1% rate, business metrics dashboards operational

---

## 12. Deployment & Infrastructure

### Environment Strategy
```yaml
# docker-compose.yml - Local development
version: '3.8'

services:
  django:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      - DATABASE_URL=postgres://user:password@postgres:5432/nexuscore
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/0
      - DEBUG=1

  nextjs:
    build: ./frontend
    command: npm run dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXT_PUBLIC_STRIPE_PUBLIC_KEY=test_pk_123

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=nexuscore
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7.4-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:

# docker-compose.production.yml - Production configuration
version: '3.8'

services:
  django:
    build: 
      context: ./backend
      dockerfile: Dockerfile.production
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/mediafiles
    depends_on:
      - postgres
      - redis
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DATABASE_URL=postgres://user:$${DB_PASSWORD}@postgres:5432/nexuscore
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    networks:
      - app_network

  celery:
    build: 
      context: ./backend
      dockerfile: Dockerfile.production
    command: celery -A config worker -l info --concurrency 4
    depends_on:
      - postgres
      - redis
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DATABASE_URL=postgres://user:$${DB_PASSWORD}@postgres:5432/nexuscore
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
    networks:
      - app_network

  nextjs:
    build: 
      context: ./frontend
      dockerfile: Dockerfile.production
      args:
        - NEXT_PUBLIC_API_URL=https://api.nexuscore.com
    command: node server.js
    networks:
      - app_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/static
      - media_volume:/media
    depends_on:
      - django
      - nextjs
    networks:
      - app_network

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=nexuscore
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=$${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network

  redis:
    image: redis:7.4-alpine
    command: redis-server --appendonly yes --maxmemory 2gb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - app_network

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:

networks:
  app_network:
    driver: bridge
```

### CI/CD Pipeline (GitHub Actions)
```yaml
# .github/workflows/deploy.yml
name: Deploy NexusCore

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7.4-alpine
        ports: ['6379:6379']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install backend dependencies
        run: |
          cd backend
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          pip install pytest pytest-django pytest-cov factory_boy
      
      - name: Run backend tests
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
          DJANGO_SETTINGS_MODULE: config.settings.test
        run: |
          cd backend
          source venv/bin/activate
          pytest --cov=. --cov-report=xml --cov-report=term
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install frontend dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run frontend tests
        run: |
          cd frontend
          npm run test:ci
          npm run lint
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: ./backend/coverage.xml

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push Django
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: nexuscore/backend:latest, nexuscore/backend:${{ github.sha }}
          cache-from: type=registry,ref=nexuscore/backend:buildcache
          cache-to: type=registry,ref=nexuscore/backend:buildcache,mode=max
      
      - name: Build and push Next.js
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          push: true
          tags: nexuscore/frontend:latest, nexuscore/frontend:${{ github.sha }}
          build-args: |
            NEXT_PUBLIC_API_URL=${{ secrets.NEXT_PUBLIC_API_URL }}

  deploy-production:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
            k8s/ingress.yaml
          images: |
            nexuscore/backend:${{ github.sha }}
            nexuscore/frontend:${{ github.sha }}
          imagepullsecrets: |
            dockerhub-secret
          namespace: nexuscore-prod
      
      - name: Run smoke tests
        run: |
          curl -s https://nexuscore.com/health
          curl -s https://api.nexuscore.com/health
```

### Monitoring & Alerting
```python
# monitoring/metrics.py - Prometheus metrics collection
from prometheus_client import Counter, Histogram, Gauge, Info
from django_prometheus.middleware import Metrics

# Business metrics
trial_signups_total = Counter('trial_signups_total', 'Total trial signups')
subscription_conversions_total = Counter('subscription_conversions_total', 'Total subscription conversions')
dsar_requests_total = Counter('dsar_requests_total', 'Total DSAR requests')

# Performance metrics
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration', ['endpoint', 'method'])
celery_task_duration = Histogram('celery_task_duration_seconds', 'Celery task duration', ['task_name'])

# System metrics
active_users = Gauge('active_users', 'Number of active users')
subscription_count = Gauge('subscription_count', 'Number of active subscriptions', ['plan'])

# Application info
app_info = Info('app_info', 'Application information')
app_info.info({
    'version': '1.0.0',
    'environment': settings.ENVIRONMENT,
    'database': settings.DATABASES['default']['ENGINE']
})

class MetricsMiddleware:
    """Django middleware for collecting business metrics"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Track trial signups
        if request.path == '/api/v1/auth/register/' and request.method == 'POST':
            response = self.get_response(request)
            if response.status_code == 201:
                trial_signups_total.inc()
                # Check if trial flag is set
                if request.data.get('trial', False):
                    trial_signups_total.labels(type='trial').inc()
            return response
        
        # Track subscription conversions
        if request.path == '/api/v1/subscriptions/' and request.method == 'POST':
            response = self.get_response(request)
            if response.status_code == 201:
                subscription_conversions_total.inc()
            return response
        
        return self.get_response(request)
```

---

## 13. Implementation Plan (12-Week Pragmatic Timeline)

### Phase 0 — Kickoff (Week 0)
**Deliverables:** Project charter, stakeholder sign-off, environment setup
- [ ] Confirm MVP scope, trial/billing policy, brand assets
- [ ] Set up GitHub repositories and CI/CD skeleton
- [ ] Provision staging infrastructure (DB, Redis, S3, domains)
- [ ] Create baseline Lighthouse report for current site (if exists)
- [ ] Finalize team roles and RACI matrix

### Phase 1 — Foundations (Sprints 1-2, Weeks 1-4)
**Deliverables:** Working dev environment, auth flows, basic marketing pages
- **Week 1-2:**
  - [ ] Bootstrap Django 6.0 project with DRF and security hardening
  - [ ] Create Next.js 14 app with Tailwind CSS and design system
  - [ ] Implement auth endpoints (register, login, verify email)
  - [ ] Set up PostgreSQL and Redis connections
  - [ ] Configure basic CI pipeline with linting and unit tests
- **Week 3-4:**
  - [ ] Implement lead capture forms with UTM tracking
  - [ ] Create Stripe sandbox integration and webhook endpoint
  - [ ] Build core marketing pages (home, features, pricing) with SSG
  - [ ] Implement basic analytics event instrumentation
  - [ ] Set up Sentry error monitoring

### Phase 2 — Core Flows (Sprints 3-4, Weeks 5-8)
**Deliverables:** Complete subscription flow, admin dashboard, background jobs
- **Week 5-6:**
  - [ ] Implement subscription creation flow (frontend + backend)
  - [ ] Build Celery workers for webhook processing and invoice generation
  - [ ] Create Django admin customizations for users and subscriptions
  - [ ] Implement invoice PDF generation and S3 storage
  - [ ] Add payment failure handling and dunning strategy
- **Week 7-8:**
  - [ ] Build DSAR endpoints and admin workflow
  - [ ] Implement demo dashboard with seeded data
  - [ ] Create resource center and blog scaffolding
  - [ ] Set up comprehensive E2E test suite (Cypress)
  - [ ] Configure Prometheus/Grafana monitoring dashboards

### Phase 3 — Polish & QA (Sprints 5-6, Weeks 9-12)
**Deliverables:** Production-ready staging environment, comprehensive testing
- **Week 9-10:**
  - [ ] Conduct accessibility audit and fix critical issues
  - [ ] Optimize performance (Lighthouse score ≥ 60 mobile)
  - [ ] Implement security hardening and CSP policies
  - [ ] Create operational runbooks and incident response plans
  - [ ] Conduct user acceptance testing with beta users
- **Week 11-12:**
  - [ ] Perform security penetration testing
  - [ ] Finalize documentation and knowledge transfer
  - [ ] Conduct load testing (1000+ concurrent users)
  - [ ] Prepare production deployment plan and rollback strategy
  - [ ] Stakeholder sign-off on launch readiness

### Phase 4 — Launch & Hardening (Weeks 13-16)
**Deliverables:** Production launch, monitoring, optimization
- **Week 13:**
  - [ ] Production deployment with blue-green strategy
  - [ ] Smoke testing and initial monitoring validation
  - [ ] Team training on operational procedures
- **Week 14-16:**
  - [ ] Performance optimization (target Lighthouse ≥ 80)
  - [ ] Post-launch bug fixes and stability improvements
  - [ ] Establish baseline KPIs and conversion metrics
  - [ ] Plan Phase 2 roadmap based on user feedback
  - [ ] Retrospective and lessons learned documentation

---

## 14. Staffing & Budget (Pragmatic Estimates)

### Team Structure (MVP Phase)
| Role | Count | Duration | Responsibilities |
|------|-------|----------|------------------|
| Lead Engineer (Backend) | 1 | 12 weeks | Django architecture, API design, security |
| Senior Backend Developer | 1 | 12 weeks | Subscription flows, Celery tasks, DSAR |
| Senior Frontend Developer | 1 | 12 weeks | Next.js implementation, performance optimization |
| UI/UX Designer | 1 | 6 weeks | Design system, component library, accessibility |
| QA Engineer | 1 | 8 weeks | Test automation, E2E testing, accessibility audit |
| Product Manager | 0.5 | 12 weeks | Requirements, sprint planning, stakeholder comms |
| DevOps Engineer | 0.5 | 4 weeks | CI/CD, monitoring, deployment automation |

### Budget Estimate (SGD)
| Category | Low Estimate | High Estimate | Notes |
|----------|-------------|--------------|-------|
| Development & Design | $60,000 | $120,000 | Based on SGD rates for Singapore talent |
| Infrastructure (Year 1) | $3,000 | $10,000 | Cloud hosting, CDN, monitoring tools |
| Third-Party Services | $1,200 | $2,400 | SendGrid, Sentry, security tools |
| Security & Compliance | $5,000 | $15,000 | Pen testing, legal review, compliance audit |
| Contingency (15%) | $10,380 | $22,110 | Buffer for scope changes and unknowns |
| **Total** | **$80,580** | **$169,510** | |

### Cost Optimization Strategies
- Use managed services (Render, Vercel) instead of full Kubernetes for initial launch
- Implement feature flags to control rollout and reduce risk
- Phase non-critical features (advanced reporting, deep integrations) to Phase 2
- Leverage open-source tools for monitoring and logging where possible

---

## 15. Risk Management & Mitigations

### Top Technical Risks
| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|-------------------|
| Payment/webhook failure | High | Critical | Idempotent processing, retry logic, monitoring + alerting, test webhooks in staging |
| Performance degradation | Medium | High | Load testing early, auto-scaling configuration, CDN optimization, phased performance targets |
| Third-party API failures | High | Medium | Circuit breakers, fallback mechanisms, vendor SLA monitoring, local development mocks |
| PDPA non-compliance | Low | Critical | Implement DSAR endpoints early, legal review, staff training, regular compliance audits |

### Business Risks
| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|-------------------|
| Delayed launch | Medium | High | Agile methodology, MVP approach, buffer time, weekly progress reviews |
| Low conversion rates | Medium | High | A/B testing framework, early user feedback, conversion optimization backlog |
| Budget overrun | Medium | Medium | Phased development, regular cost tracking, scope prioritization framework |
| Talent availability | Low | High | Cross-training team members, documentation focus, vendor partnerships |

### Contingency Plans
- **Timeline pressure:** Defer non-critical features (advanced reporting, deep integrations) to Phase 2
- **Budget constraints:** Use managed services instead of self-hosted solutions, reduce scope to core flows only
- **Technical blockers:** Implement feature flags to disable problematic features, maintain rollback capability
- **Compliance issues:** Engage legal counsel early, implement DSAR workflow before launch, document all data flows

---

## 16. Acceptance Criteria (Launch Readiness)

### Functional Requirements
- [ ] Visitor can sign up, verify email, and access demo dashboard with seeded data
- [ ] Visitor can start a trial and/or subscribe via Stripe; Stripe webhooks update app state reliably
- [ ] Lead forms create a `lead` record with UTM data and send CRM webhook
- [ ] Admin can view users, subscriptions, invoices in Django Admin and export CSV
- [ ] DSAR requests are processed within 72 hours with automated notifications

### Non-Functional Requirements
- [ ] CI pipeline runs when PRs are created; staging deploy completes automatically
- [ ] Core Web Vitals: Mobile LCP ≤ 2.5s (launch), accessibility score ≥ 90 for primary flows
- [ ] Monitoring/alerts configured for webhook failures and worker backlogs
- [ ] Penetration test completed with no critical findings
- [ ] Runbooks documented for payment failures, DSAR processing, and incident response

### Security Requirements
- [ ] No high-severity issues in static dependency scanning
- [ ] HTTPS enforced, CSP/HSTS headers present, secrets not stored in code
- [ ] Password policy enforced with rate limiting
- [ ] Audit logs maintained for all sensitive operations
- [ ] Regular security updates and vulnerability patching process documented

---

## 17. Deliverables (MVP)

### Code & Configuration
- Next.js marketing site with design system and components
- Django 6.0 + DRF backend with auth, subscription & invoice endpoints
- Celery-based background processing for webhooks & email
- Stripe integration (sandbox & production configurations)
- Monitoring & alerting setup (Sentry, Prometheus + Grafana template)

### Documentation
- API specification (OpenAPI/Swagger)
- Deployment guide with environment setup instructions
- DSAR process documentation and legal compliance guide
- Operational runbooks for payment failures and critical incidents
- Architecture decision records (ADRs) for key technical choices

### Testing & Quality
- Unit test coverage ≥ 70% for critical backend modules
- E2E test suite covering core user journeys
- Accessibility audit report with remediation plan
- Performance benchmark report with optimization roadmap
- Security assessment report with findings and remediation status

---

## 18. Next Steps & Immediate Actions

### Week 0 Actions
- [ ] **Kickoff meeting:** 2-hour stakeholder session to finalize trial rules, PSP decision, and KPI targets
- [ ] **Baseline audits:** Run Lighthouse and accessibility scans on current site (if any) to set baseline
- [ ] **Repository setup:** Create GitHub repos with proper structure and branch protection rules
- [ ] **Infrastructure provisioning:** Set up staging environments for PostgreSQL, Redis, and S3
- [ ] **Team onboarding:** Share PRD with development team, conduct technical deep-dive session

### Week 1-2 Actions
- [ ] **Django 6.0 setup:** Initialize project with security hardening and DRF configuration
- [ ] **Next.js 14 setup:** Create app with Tailwind CSS and component library foundation
- [ ] **Auth flow implementation:** Build register/login/verify email endpoints and UI
- [ ] **Stripe sandbox integration:** Configure test accounts and webhook endpoints
- [ ] **CI pipeline configuration:** Set up GitHub Actions for linting, tests, and staging deployment

This PRD serves as a complete, production-ready blueprint for building the NexusCore platform. It balances strategic vision with pragmatic execution, ensuring we deliver a high-quality, maintainable solution that meets business goals while adhering to technical best practices and compliance requirements. The focus on Django 6.0 provides a modern, secure foundation that will scale with our business needs.
