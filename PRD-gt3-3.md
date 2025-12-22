# Project Requirements Document (PRD) — Drop-in Replacement
**Project Name:** NexusCore (drop-in replacement — pragmatic, production-ready)  
**Version:** 1.2 (merged, pragmatic, English-only)  
**Date:** 2025-12-22  
**Primary Objective:** Build a production-grade marketing + lead-management + demo/trial website for a Singapore-based medium B2B SaaS company. The solution must be pragmatic, secure, accessible (WCAG AA for primary flows), and easy to operate. The backend uses **Django 6.0 + DRF**; frontend is **Next.js 14.2+** (React 18 + TypeScript). DB: **PostgreSQL 16+**, Cache/Broker: **Redis 7.4+**, Python 3.12+.

---

# 1. Executive summary
Deliver an English-only, high-converting marketing and trial platform that replaces a generic template. It must:
- Convert visitors into qualified leads and trial users.
- Provide a safe, auditable subscription & billing surface (Stripe-first, PayNow optional).
- Ship quickly (MVP within 12 weeks) and be maintainable by a small engineering team.
- Meet Singapore PDPA requirements for consent and DSARs.

Primary outcome metrics: trial signup conversion, demo requests, MQL → SQL velocity, Core Web Vitals.

---

# 2. Core goals & success metrics

**Business goals**
- Generate qualified leads and reduce friction to trial/demo.
- Provide marketing & sales with measurable funnel events.
- Run a reliable billing/trial pipeline for revenue capture.

**Success metrics (initial 90-day targets)**
- Trial/Demo signups: baseline → +30% within 90 days after launch.
- Conversion (visitor → primary CTA click): ≥ 5% on pricing pages.
- Core Web Vitals: Mobile LCP ≤ 2.5s (launch) → ≤ 2.0s within 60 days.
- Accessibility: No critical WCAG AA failures for signup/checkout flows.
- Payment reliability: webhook processing success rate ≥ 99.9%.

---

# 3. Scope (MVP vs Future)

**MVP (in-scope)**
- Marketing pages (home, features, pricing, case studies, FAQ, blog/resource center).
- Signup, email verification, password reset.
- Trial sign-up with demo dataset (no production tenant multi-tenancy).
- Subscription flow integrated with Stripe (monthly/annual, trial handling).
- Lead capture forms with UTM capture and CRM webhook.
- Admin (Django Admin + minimal admin UI) for users, subscriptions, invoices.
- Background jobs via Celery for webhooks, emails, invoice generation.
- Analytics event instrumentation (GA4 + server-side forwarding).
- Basic PDPA compliance: cookie consent, marketing opt-in, DSAR endpoints.
- CI/CD pipelines, monitoring (Sentry), and basic runbooks.

**Out of scope (MVP)**
- Full-feature accounting (ERP) and deep inventory—only a "demo" read-only mock of invoicing/inventory.
- Enterprise SSO beyond one SAML/OAuth example.
- Multi-region hosting or advanced multi-tenancy (phase 2).

---

# 4. Tech stack & rationale

**Backend**
- Django 6.0 (Python 3.12+), Django REST Framework (latest compatible).
- Celery 5.x (broker Redis 7.4+), django-tasks for lightweight scheduled jobs.
- PostgreSQL 16+ for primary data store.
- Redis 7.4+ for caching, sessions (optional), and Celery broker.

**Frontend**
- Next.js 14.2+ (App Router), React 18, TypeScript.
- Tailwind CSS (or design-team preferred CSS system) for component styling and performance.
- ISR/SSG for marketing pages; SSR for dynamic pages where necessary.

**Other**
- Stripe (payments), SendGrid or AWS SES (email), Sentry (error monitoring), Prometheus + Grafana (metrics).
- Storage: S3-compatible object storage for invoice PDFs, assets.
- CI/CD: GitHub Actions for tests/builds; deploy to chosen cloud (AWS, GCP, or Vercel for front-end).

Rationale: strong developer ergonomics, predictable infrastructure, and ready observability.

---

# 5. High-level architecture

```

[User Browser] -> Next.js (SSR/SSG) -> DRF API (HTTPS) -> Django Business Logic
|
v
PostgreSQL 16
|
Redis 7.4
|
Celery
|
Third-party: Stripe, SendGrid, CRM, CDN

```

Key constraints: secure APIs (TLS), idempotent webhook processing, safe storage of PII, documented data flows for compliance.

---

# 6. Major user journeys

1. **Discovery → Trial**
   - User lands on marketing page → reads features → toggles pricing → clicks "Start free trial" → fills form → receives verification → redirected to demo dashboard with seeded data.

2. **Discovery → Request Demo**
   - User completes demo request → creates CRM lead with UTM tags → sales notified (email/Slack) → auto follow-up workflow.

3. **Signup → Subscribe**
   - User signs up, chooses plan, enters payment via Stripe → payment validated → subscription activated → invoice emailed and stored.

4. **Admin Operations**
   - Admin views/cancels subscription, issues refund, exports CSV, views audit logs.

5. **DSAR / Privacy Request**
   - User requests data export or deletion → system creates DSAR package for admin review and execution.

---

# 7. Data model (core entities — pragmatic)

Primary tables (simplified):
- `users` (id, email, password_hash, name, role, is_active, created_at, last_login)
- `organizations` (id, name, stripe_customer_id, timezone, billing_contact)
- `subscriptions` (id, org_id, plan_id, status, started_at, current_period_end, stripe_id)
- `plans` (id, name, price_monthly, price_annual, features_json)
- `invoices` (id, org_id, amount, currency, status, pdf_url, stripe_invoice_id, created_at)
- `leads` (id, name, email, company, source, utm, created_at)
- `audit_logs` (id, user_id, action, resource_type, resource_id, metadata, created_at)
- `events` (id, event_type, org_id, user_id, payload_json, created_at)
- `dsar_requests` (id, user_email, request_type, status, export_url, requested_at, processed_at)

Indexes: index subscriptions and invoices by org_id; events should use time-based partitioning when volume grows.

---

# 8. API surface (selected, pragmatic)

Use HTTPS, JSON, and token-based auth for API. Protect admin endpoints.

**Auth**
```

POST  /api/v1/auth/register/       { email, password, name, org_name? }
POST  /api/v1/auth/login/          { email, password } -> { access_token, refresh_token }
POST  /api/v1/auth/refresh/        { refresh_token }
POST  /api/v1/auth/verify-email/   { token }
POST  /api/v1/auth/password-reset/ { token, new_password }

```

**Subscription & billing**
```

GET  /api/v1/plans/
POST /api/v1/subscriptions/             { org_id, plan_id, payment_method_id, coupon? }
GET  /api/v1/subscriptions/{id}/
POST /api/v1/subscriptions/{id}/cancel/ { effective_immediate: bool }
POST /api/v1/subscriptions/{id}/change/ { new_plan_id }
GET  /api/v1/invoices/                  ?org_id=
GET  /api/v1/invoices/{id}/download/    -> PDF

```

**Leads & demo**
```

POST /api/v1/leads/           { name, email, company, message, utm_source, utm_medium, utm_campaign }
POST /api/v1/demo-request/    { name, email, company, preferred_time, timezone, utm_* }

```

**Webhooks**
```

POST /api/v1/webhooks/stripe/   { stripe_signature_header } -> verify, enqueue processing

```

**DSAR**
```

POST /api/v1/dsar/submit/       { email, request_type } -> { dsar_id }
GET  /api/v1/dsar/status/{id}/

```

Design notes:
- Webhooks must validate signature and be idempotent.
- Use idempotency keys for subscription creation.

---

# 9. Background jobs (Celery tasks — prioritized)

**Queues**
- `high` — webhook processing, billing actions
- `default` — transactional emails, invoice generation
- `low` — reports, exports

**Tasks**
- `process_stripe_webhook(payload)` — validate & update subscription/invoice status, enqueue follow-ups.
- `generate_invoice_pdf(invoice_id)` — render HTML → PDF → S3 store.
- `send_transactional_email(template, to, context)` — queued mail sending.
- `billing_retry_job()` — scheduled job implementing dunning.
- `daily_reports()` — send admin summary emails.
- `process_dsar_request(dsar_id)` — gather user data into export package and notify admin.
- `cleanup_temp_files()` — housekeeping.

Retry policies: exponential backoff; webhook idempotency to avoid double-charging.

---

# 10. UX & design system (pragmatic)

**Principles**
- Performance-first: small bundle sizes, critical CSS, defer non-critical scripts.
- Accessibility-first: semantic HTML, keyboard navigation, visible focus states.
- Clarity & conversion: concise hero, pricing clarity, minimal form friction.

**Core components**
- `Hero` (headline, subhead, 2 CTAs)
- `FeatureCard` (icon, title, one-line benefit)
- `PricingCard` (tier badge, price, features, CTA)
- `Testimonial` & `LogoGrid`
- `FAQAccordion` (ARIA compliant)
- `LeadForm` (multi-step optional)
- `DemoDashboardPreview` (client-side mock data, non-sensitive)

**Tokens**
- Typography: Inter (H1 48px/3rem, H2 32px/2rem, body 16px/1rem)
- Spacing: base 4px scale; use 8/16/24/32px for common gaps
- Color: primary (brand) — accessible contrast values; focus ring color distinct and accessible

---

# 11. Accessibility & internationalization

**Accessibility**
- Target WCAG 2.1 AA for primary flows (signup, checkout, pricing, demo).
- Automated checks: axe-core during CI and periodic manual audits.
- Keyboard-only flows: able to complete signup and subscribe.
- Alt text policy: all meaningful images must have alt; decorative images `role="img"` with `aria-hidden="true"`.

**Internationalization**
- English-only for launch. Codebase prepared for i18n (Next.js i18n routing & Django gettext) for future localization.

---

# 12. Security & compliance (PDPA-focused)

**Application security**
- Django security middleware + HTTPS, HSTS, CSP headers.
- Parameterized ORM queries; avoid raw SQL.
- CSRF protection for cookie-based flows; use secure cookies.
- Password policy: min length + rate limiting + optional 2FA for admin users.
- Secrets in vault (e.g., cloud secrets manager).

**Payments**
- Use Stripe tokenization; do not store card numbers.
- Webhook keys kept secret; verify signatures.

**PDPA & DSAR**
- Consent capture on forms (explicit opt-in for marketing).
- DSAR endpoints and admin workflow (export within 72 hours).
- Data retention policy: PII retention windows documented; deletion endpoints with audit logs.

**Pen testing**
- External penetration test pre-launch (or in Phase 4) for high-risk flows (auth, payments).

---

# 13. Testing strategy

**Automated**
- Backend unit tests (Django): model, serializer, business logic.
- API tests (DRF): use pytest + factory_boy.
- Frontend unit tests: Jest + React Testing Library.
- E2E: Cypress covering signup → verification → subscription → invoice download → DSAR.
- Accessibility checks: axe-core in CI.

**Manual**
- Cross-browser testing (Chrome, Safari, Edge) and mobile device checks.
- Payment scenarios: success, failed card, chargeback simulation.
- Keyboard-only navigation tests and screen-reader (NVDA/VoiceOver) sanity checks.

**Acceptance tests (examples)**
- `test_end_to_end_subscription_flow()` passes in staging with simulated Stripe webhooks.
- `test_dsar_export_with_user_email()` produces data package and updates DSAR status.

---

# 14. Analytics & measurement (event taxonomy)

**Minimum event list**
- `page_view` (path, utm_*)
- `cta_click` (cta_name, page)
- `lead_submitted` (lead_id, source, utm_*)
- `trial_started` (user_id, org_id, plan_id)
- `subscription_created` (subscription_id, plan_id)
- `invoice_generated` (invoice_id, amount)
- `dsar_requested` (dsar_id, email)

Design: send critical events client-side to GA4 and duplicate server-side event for revenue-critical events to avoid loss due to ad-blockers.

**Dashboards**
- Marketing funnel dashboard (acquisition → trial → paid).
- Payment health dashboard (webhook success/failure, retry count).
- DSAR queue & SLA dashboard.

---

# 15. Deployment & infrastructure (pragmatic)

**Environments**
- `dev`, `staging`, `prod` — mirrored configs; staging connected to test Stripe account.

**Deployment pattern**
- Containerized apps (Docker); front-end deployed to Vercel (preferred) or CDN-backed S3 + Cloudfront.
- Backend deploys to managed Kubernetes or App Service; small teams may choose managed services (Render, Fly.io).
- IaC: Terraform for infra (networks, DB, IAM).

**CI/CD**
- GitHub Actions:
  - PR: lint, unit tests, type checks
  - Main→staging: run tests, deploy to staging
  - Main→production: gated deploy with manual approval and smoke tests

**Secrets & config**
- Store secrets in cloud secrets manager, do not place in repo.
- Use environment-specific settings and feature flags.

---

# 16. Monitoring & runbook

**Monitoring**
- Error tracking: Sentry
- Metrics: Prometheus (API latency, queue depth), Grafana dashboards
- Logs: structured logs shipped to cloud logging (ELK or managed)
- Synthetic checks: health endpoint and user journey checks (signup, login)

**Alerts**
- High error rate (>1% of requests)
- Celery queue backlog > threshold
- Failed webhook processing > threshold
- Payment failure spikes

**Runbook highlights**
- Payment webhook failure: investigate last webhook → check idempotency keys → re-process → notify finance and sales.
- DSAR overdue: escalate to Legal & CTO, notify data protection officer.

---

# 17. Roadmap & phased delivery (pragmatic 12 + 4 weeks)

**Assumptions**
- Team: 2 frontend devs, 2 backend devs, 1 designer, 1 QA, 0.5 PM (part-time), 0.5 DevOps
- 2-week sprint cadence.

**Phase 0 — Kickoff (Week 0)**
- Confirm trial policy, billing rules, branding assets, and stakeholder sign-off on MVP scope.

**Phase 1 — Foundations (Sprints 1–2, Weeks 1–4)**
- Infra provisioning, repo & CI, Django skeleton & DRF, Next.js skeleton, auth flows, DB schemas, Stripe sandbox integration, lead form endpoint, basic marketing pages (SSG).

**Phase 2 — Core Flows (Sprints 3–4, Weeks 5–8)**
- Pricing pages and subscription UI, webhook handlers, Celery tasks, invoice generation (PDF), admin user & subscription views, analytics instrumentation.

**Phase 3 — Polish & QA (Sprints 5–6, Weeks 9–12)**
- Demo dashboard with seeded data, resource center, blog scaffolding, DSAR endpoints, accessibility fixes, performance optimizations, E2E tests, staging hardening.

**Phase 4 — Launch & Hardening (Weeks 13–16)**
- Production launch, monitoring tuning, penetration test (as feasible), post-launch fixes, baseline KPI measurement, backlog iteration.

---

# 18. Staffing & budget (pragmatic estimate)

**Team (recommended for MVP)**
- 2 × Frontend engineers (Next.js) — 12 weeks
- 2 × Backend engineers (Django/DRF) — 12 weeks
- 1 × Designer (UI/UX) — 8 weeks (sprints 1–4)
- 1 × QA — 8–10 weeks (from Sprint 3)
- 0.5 × PM / Product Owner — full project
- 0.5 × DevOps/Infra — Week 1 & deployment phases

**Budget ballpark (SGD)**
- Development & design: SGD 60k — 120k (team rates vary)
- Infra & SaaS (first-year): SGD 3k — 10k (hosting, Stripe fees, SendGrid/Sentry)
- Contingency: 15%

Provide a detailed cost breakdown in a separate workbook if required.

---

# 19. Risk register & mitigations

1. **Payment/webhook failure (High)**  
   - Mitigation: Idempotent processing, retry logic, monitoring + alerting, test webhooks in staging.

2. **Performance on mobile (High)**  
   - Mitigation: SSG/ISR for landing pages, critical CSS, defer third-party scripts, measure & iterate.

3. **Compliance & DSAR misses (Medium)**  
   - Mitigation: Implement DSAR endpoints, staff SLAs, audit logs, legal review.

4. **Scope creep for accounting/inventory (Medium)**  
   - Mitigation: Keep demo-only for MVP; define explicit scope and acceptance.

---

# 20. Acceptance criteria (must-have for launch)

- **Functional**
  - Visitor can sign up, verify email, and access demo dashboard with seeded data.
  - Visitor can start a trial and/or subscribe via Stripe; Stripe webhooks update app state reliably.
  - Lead forms create a `lead` record with UTM data and send CRM webhook.
  - Admin can view users, subscriptions, invoices in Django Admin and export CSV.

- **Non-functional**
  - CI pipeline runs when PRs are created; staging deploy completes automatically.
  - Core Web Vitals: Mobile LCP ≤ 2.5s (launch), accessibility score ≥ 90 for primary flows in Lighthouse.
  - DSAR submission produces an export package within 72 hours (automated task initiated).
  - Monitoring/alerts configured for webhook failures and worker backlogs.

- **Security**
  - No high-severity issues in static dependency scanning.
  - HTTPS enforced, CSP/HSTS headers present, secrets not stored in code.

---

# 21. Deliverables (MVP)

- Next.js marketing site with design system and components.
- Django 6.0 + DRF backend with auth, subscription & invoice endpoints.
- Celery-based background processing for webhooks & email.
- Stripe integration (sandbox & production configurations).
- Admin + basic operational runbook.
- Test suites: unit + integration + E2E for critical flows.
- Monitoring & alerting setup (Sentry, Prometheus + Grafana template).
- Documentation: API spec, deployment guide, DSAR process, runbooks.

---

# 22. Implementation checklist (first 30 days)

**Week 0**
- [ ] Confirm MVP scope, sign-off on trial/billing policy, brand assets collected.
- [ ] Create repo & CI skeleton; infra planning session.

**Week 1–2**
- [ ] Provision staging infra (DB, Redis, S3, staging domain).
- [ ] Bootstrap Django 6.0 project + DRF; basic auth endpoints.
- [ ] Bootstrap Next.js app (App Router) with base pages and global header/footer.
- [ ] Connect staging to Stripe test account.

**Week 3–4**
- [ ] Implement subscription create flow (frontend checkout → backend create customer & subscription with idempotency).
- [ ] Implement Stripe webhook endpoint + Celery worker to process events.
- [ ] Implement lead capture endpoint and CRM webhook.
- [ ] Initial Lighthouse audit and performance backlog.
