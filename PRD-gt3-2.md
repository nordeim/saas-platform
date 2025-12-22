# 1) Short verdict

Your PRD is strategically strong (market context, personas, UX/system thinking) and more commercially detailed (budget, timeline, KPIs) than my original draft. My PRD supplied more implementation-level technical specifics (API endpoints, background jobs, queue strategy, devops/observability checklist) and operational acceptance criteria. Combined, the two PRDs cover strategy → implementation very well; merging them yields a production-ready blueprint.

---

# 2) Major areas of agreement

* **Headless decoupled architecture** (Next.js frontend + Django/DRF backend) — identical.
* **Core tech choices** (Postgres, Redis, Celery, Next.js App Router, TypeScript) — aligned.
* **Primary flows** (marketing pages → trial/demo → subscription + admin) — identical.
* **Accessibility, SEO, performance & PDPA compliance** as hard requirements — aligned.
* **Must-have components** (hero, features, pricing, case studies, FAQ, blog/resource center) — aligned.

---

# 3) Strengths of *your* PRD vs mine

* **Market specificity & localization** — excellent inclusion of PSG/EDG grants, PayNow, and SEA-focused positioning. This adds strong commercial context for GTM and sales enablement.
* **Detailed UI/UX specs** — specific typography, grid, color token choices, and page-by-page components are well-defined and useful for designers.
* **Budget & timeline** — practical cost ranges and a 16-week roadmap with weekly phase breakdown; helpful for stakeholder commitments and procurement.
* **Tighter performance targets** — explicit Lighthouse >90 and <2s PFP targets give clear goals (though see feasibility note below).
* **Concrete KPIs (acquisition/engagement/conversion)** — business-targeted metrics help align marketing & product.

---

# 4) Strengths of *my* PRD that complement yours

* **Implementation-level details**: explicit API endpoints, Celery task list, queue priorities, invoice PDF generation, webhook handling. These reduce ambiguity for engineers.
* **Operational runbooks & monitoring**: Sentry/Prometheus/Grafana, queue monitoring, health checks — practical for ops readiness.
* **Testing & QA specifics**: suggested E2E tests, Cypress examples, acceptance tests for billing/webhooks.
* **Data model & entity definitions**: high-level ER mapping and indexing notes that aid DB design.
* **Risk mitigation specifics**: e.g., idempotency for webhooks, dunning strategy, and scope-limiting for accounting/inventory features.

---

# 5) Key differences to reconcile (and why they matter)

1. **Performance target realism**

   * Your PRD: Lighthouse >90 across the board, FCP <2s on 4G.
   * My PRD: Targets but phased improvements (initial ≥60, then improve).
   * **Why it matters:** >90 is achievable but often requires effort and trade-offs (asset strategy, third-party scripts, careful SSR/ISR). I recommend a phased target: baseline → quick wins → stretch goal >90 post-launch.

2. **Budget & resourcing detail**

   * Your PRD gives cost ranges but lacks staffing breakdown (FTEs, contractor-hours) and third-party recurring costs.
   * **Why it matters:** Accurate budgeting needs clear assumptions about rates, number of design/dev sprints, cloud & SaaS costs (Stripe fees, SendGrid, CDN), and post-launch support.

3. **Operational granularity**

   * My PRD includes background jobs, webhook processing, and admin export requirements in detail; your PRD references them but with less technical acceptance criteria.
   * **Why it matters:** Billing and webhooks are revenue-critical — they should have precise acceptance tests and monitoring.

4. **Analytics & experimentation**

   * You mention analytics and personalization phases; my PRD includes concrete event names and instrumentation suggestions.
   * **Why it matters:** Without an event taxonomy and measurement plan, conversion and A/B testing will be slow to iterate.

5. **Compliance & DSAR workflows**

   * Your PRD cites PDPA and consent — good — but lacks a DSAR process, deletion/export endpoints, and retention policy specifics.
   * **Why it matters:** DSARs and deletion are operational/legal tasks that need endpoints, logs, and SLA for response.

6. **Payment localization**

   * You added PayNow — great. My PRD recommended Stripe as primary PSP and noted potential connectors.
   * **Why it matters:** PayNow/PayPal/Stripe involve different settlement flows and reconciliation; include reconciliation and reporting tasks.

---

# 6) Missing or under-specified items you should add (high-value)

1. **Event taxonomy & measurement plan** — list of events, properties, UTM usage, reporting dashboards, baseline metrics.
2. **Acceptance tests for financial flows** — simulate Stripe webhooks, retries, proration, refunds, idempotency.
3. **DSAR endpoints & process** — `/api/v1/dsar/export/` and `/api/v1/dsar/delete/`, internal SLAs.
4. **Operational costs & 12-month run-rate** — hosting, CDN, email, monitoring, backup, support.
5. **Staffing & RACI** — who owns each deliverable and who signs off (PM, Eng lead, Designer, Security).
6. **Detailed content migration / CMS model** — fields, templates, and authoring flows (preview, publish schedule).
7. **Third-party script governance** — policy for GTM/analytics/marketing pixels and their impact on performance/privacy.
8. **A/B testing plan** — first 3 experiments, metrics, sample size estimates.
9. **Incident & rollback playbook** — who does what when billing/webhook failures occur.

---

# 7) Feasibility & risk notes (practical realities)

* **Lighthouse >90**: Achievable for marketing pages if you control third-party scripts, optimize images, use ISR/SSG, and limit client bundles. For interactive dashboard pages, expect higher client-side JS; target separate thresholds.
* **16-week timeline**: Reasonable for MVP marketing + trial flows if you have a small focused team (1–2 FE devs, 1–2 BE devs, 1 designer, 1 PM, 1 QA). If resource-constrained, phase scope or extend schedule.
* **Budget variance**: The provided ranges are plausible but can swing based on UX complexity, animations, number of integrations, and localization work. Include a clear assumptions appendix for the estimate.

---

# 8) Concrete prioritized recommendations (immediate & next 30–60 days)

**Top-priority (do these first)**

1. **Finalize product & billing policy** — trial length, whether card required, proration rules, refund rules. (Owner: PO) — *Acceptance:* documented policy signed off.
2. **Create event taxonomy & measurement plan** — map events to KPIs. (Owner: Growth/Analytics) — *Acceptance:* event sheet + dashboard templates.
3. **Define DSAR & retention policy** — document data flows and endpoints. (Owner: Legal/CTO) — *Acceptance:* DSAR process doc + API endpoint list.
4. **Baseline performance audit** — run Lighthouse and list top 10 fixes. (Owner: Eng Lead) — *Acceptance:* Lighthouse report + remediation backlog.

**Medium priority**
5. **Add financial flow acceptance tests** — include webhook idempotency and dunning scenarios. (Owner: BE lead + QA)
6. **Define staffing & RACI** — convert budget into people and sprint capacity. (Owner: PM)
7. **Add cost-of-ownership table** — 12-month run-rate for infra & SaaS. (Owner: Ops/Finance)

**Lower priority (iterative)**
8. **A/B testing roadmap** — define hypotheses and measurement windows.
9. **Detailed content migration plan** — field map and editorial schedule.
10. **Accessibility certification checklist** — map to WCAG A/AA tests and manual checks.

---

# 9) Suggested acceptance criteria you should add (examples)

* **Subscription end-to-end**: user signs up → enters payment → Stripe webhook fires → subscription becomes `active` → invoice generated & downloadable PDF available. (Automated E2E)
* **Performance baseline**: Home page mobile LCP ≤ 2.5s at launch, then improve to ≤ 2s within 8 weeks.
* **Accessibility**: No WCAG AA contrast failures for primary flows; keyboard-only flow completes signup and plan purchase.
* **DSAR SLA**: Export DSAR package ≤ 72 hours; deletion processed within 7 days and logged.

---

# 10) Minimal merged deliverables I recommend producing next (I can create any one now)

1. **Implementation Playbook** — merged PRD → phase-by-phase tasks, owners, acceptance criteria, sprint backlog seeds.
2. **Technical Spec** — API surface, Celery jobs, DB schema, webhook handling, monitoring & runbooks.
3. **Analytics & Experiment Plan** — event taxonomy, dashboards, initial A/B tests.
4. **Cost & Resourcing Workbook** — convert budget ranges into roles, hourly estimates and 12-month run-rate.

(If you want, I’ll produce deliverable #1 — Implementation Playbook — right now and include acceptance criteria and an initial 6-sprint backlog.)

---

# 11) Closing

Add an **Events & Acceptance Matrix** to the PRD: for each major user flow (signup, trial start, subscription change, invoice download, demo request) list the required backend APIs, Celery tasks, monitoring alerts, E2E tests, and business KPI that proves the flow. This single addition closes the gap between strategy and engineering acceptance.

---

# Project Requirements Document (PRD) — Drop-in Replacement

**Project Name:** NexusCore — English-only SaaS Corporate Website & Marketing Platform (Pragmatic Production Release)
**Version:** 1.0 (merged + pragmatic)
**Date:** 2025-12-22
**Primary Stack:**

* **Backend:** Django 6.0 + Django REST Framework (DRF) + Celery + django-tasks
* **Frontend:** Next.js 14.2+ (App Router) + React 18 + TypeScript
* **DB / Cache:** PostgreSQL 16+, Redis 7.4+
* **Python:** 3.12+
* **Hosting/Infra:** Containerized (Docker) -> Cloud (managed K8s or managed App Service) + CDN (Cloudfront / Cloudflare / Fastly)
* **Primary PSP:** Stripe (SGD + PayNow via Stripe where supported)

---

# Executive summary

Build a production-ready, English-only marketing & lead-management site for a Singapore-based medium B2B SaaS company. This is a **drop-in replacement PRD** that merges strategic market context, design guidance, and concrete engineering deliverables into a pragmatic, implementable plan. The MVP focuses on marketing pages, lead capture, trial onboarding, subscription billing, and an admin for operations. Accessibility (WCAG AA), performance (pragmatic Core Web Vitals), security, and PDPA-compliant data handling are non-negotiable.

Primary goals:

* Convert visitors → qualified leads → trials/demos with measurable funnels.
* Provide robust subscription and invoice flows with production-grade webhook and retry handling.
* Ship within a practical phased delivery (MVP in 10–12 weeks with phased enhancements).
* Maintainable, secure, and testable architecture for rapid iteration.

---

# Key stakeholders & roles

* **Executive Sponsor / PO** — business decisions, acceptance of scope & KPI targets
* **Product Manager (PM)** — day-to-day prioritization, sprint planning, stakeholder communication
* **Lead Engineer (BE)** — Django/DRF code ownership, infra decisions
* **Lead Engineer (FE)** — Next.js, component library, performance ownership
* **Designer / UX** — design system, accessible UI components, copy work with Marketing
* **QA Engineer** — automated + manual testing, accessibility testing
* **DevOps / SRE** — CI/CD, monitoring, backups, runbooks
* **Marketing Owner** — content, SEO, UTM & analytics strategy
* **Sales/CS Owner** — lead handoff, demo scheduling, CRM rules

---

# Scope — MVP vs Future

**MVP (in-scope)**

* Public marketing pages: Home, Product/Solutions, Pricing, Case Studies, Resources (blog), Contact, Privacy/Terms, FAQ
* Lead capture forms (UTM capture), demo-request flow, newsletter sign-up
* User auth: email signup, verify, password reset, simple trial onboarding
* Subscription & Billing: Stripe integration (trial, starter, pro); invoice generation and PDF; webhook processing + Celery tasks
* Admin dashboard (Django admin + lightweight custom admin pages): users, leads, subscriptions, invoices, exports
* Demo-only product screens (read-only mockups of accounting/inventory features)
* Instrumentation: GA4 + server-side event forwarding (basic)
* Performance: SSG/ISR for marketing pages, image optimization, CDN usage
* Accessibility: WCAG AA for primary flows

**Out of MVP / phased later**

* Full ERP-level accounting/inventory modules (only demo mockups in MVP)
* Enterprise SSO beyond OAuth/SAML (can be planned)
* Deep personalization + multi-language support (English-only initial)
* Advanced CRM two-way sync (basic outbound webhooks in MVP)

---

# High-level user journeys

1. Visitor → Home → reads features → Pricing → starts trial or requests demo → completes sign-up → receives verification → enters product demo.
2. Visitor → Reads case study → requests quote/demo → sales receives lead with UTM and context.
3. Admin → Reviews new leads → converts to demo scheduling → monitors subscriptions & invoices.

---

# Architecture (logical / pragmatic)

```
            CDN (images, assets)
                 ▲
                 |
            Next.js (App Router)  <--->  Public SSG/ISR pages
                 |
    Client (browser) -> Auth -> API calls
                 |
         HTTPS / REST (JSON) / GraphQL (future)
                 |
           Django 6.0 + DRF (API)  <--->  PostgreSQL 16
                 |                         |
            Celery workers  <------------ Redis 7.4  (broker + cache)
                 |
       Background tasks: webhooks, invoices, emails
                 |
            S3-compatible storage for uploaded files & invoice PDFs
```

Key design choices:

* Marketing pages: SSG/ISR via Next.js for speed/SEO.
* Dynamic user flows: SSR or client fetch from DRF as needed.
* Authentication: session cookies with HTTP-only secure cookies OR short-lived JWT with refresh token depending on ops preference. Recommend secure cookies for web flows.
* Celery with Redis broker; separate queues for high-priority (webhooks/billing), default (emails) and low (reports).

---

# Event taxonomy & Acceptance Matrix (critical — implement immediately)

| Flow                  |               Event Name | Key properties                              | Success criteria / Acceptance test                                                     |
| --------------------- | -----------------------: | ------------------------------------------- | -------------------------------------------------------------------------------------- |
| Visitor page view     |              `page_view` | `page`, `url`, `utm_source`, `device`       | Event recorded server-side/GA4 on every page view; sample export available             |
| Hero CTA click        |              `cta_click` | `cta_id`, `page`, `user_id?`                | Click recorded; UI shows expected modal/redirect                                       |
| Demo request          | `demo_request_submitted` | `lead_id`, `email`, `utm`                   | Lead saved in DB; webhook to CRM fired; sales notified                                 |
| Trial signup          |          `trial_started` | `user_id`, `org_id`, `plan_id`              | User created, trial flag set, confirmation email queued & sent                         |
| Subscription created  |   `subscription_created` | `subscription_id`, `stripe_id`, `amount`    | Subscription active after Stripe webhook archived; invoice generated                   |
| Invoice paid          |           `invoice_paid` | `invoice_id`, `amount`, `stripe_invoice_id` | Celery webhook processed idempotently; invoice status `paid`                           |
| DSAR export requested |           `dsar_request` | `user_id`, `request_id`                     | DSAR package created within SLA (≤72 hours) and link/email sent                        |
| Payment failure       |         `payment_failed` | `subscription_id`, `reason`                 | Dunning tasks start; notifications sent; monitoring alert triggered if retries exhaust |

Acceptance Matrix example for `subscription_created`:

* POST `/api/v1/subscriptions/` with card token => DRF returns 201 and `subscription_id`.
* Stripe creates subscription => Stripe webhook `invoice.payment_succeeded` received. Webhook processed by Celery `process_stripe_webhook` task, idempotency key used. DB subscription becomes `active`. Invoice PDF generated and uploaded to S3. Notification email sent. End-to-end E2E test passes.

---

# API surface (selected — pragmatic & concrete)

All endpoints under `/api/v1/` with HTTPS and JSON.

**Auth**

```
POST /api/v1/auth/register/          { email, password, company_name, plan_id? } -> 201
POST /api/v1/auth/login/             { email, password } -> session cookie or tokens
POST /api/v1/auth/logout/
POST /api/v1/auth/verify-email/      { token }
POST /api/v1/auth/password-reset/    { token, new_password }
```

**Leads & Contact**

```
POST /api/v1/leads/                  { name, email, company, role, utm... } -> lead_id
GET  /api/v1/leads/?status=new       (admin)
POST /api/v1/leads/{id}/assign/      { owner_id }
```

**Subscriptions & Billing**

```
GET  /api/v1/plans/
POST /api/v1/subscriptions/          { org_id, plan_id, payment_method_id }
GET  /api/v1/subscriptions/{id}/
POST /api/v1/subscriptions/{id}/cancel/
POST /api/v1/subscriptions/{id}/change-plan/ { plan_id }
GET  /api/v1/invoices/
GET  /api/v1/invoices/{id}/download/  (PDF)
```

**Webhooks**

```
POST /api/v1/webhooks/stripe/        (verify signature, enqueue)
```

**DSAR & Privacy**

```
POST /api/v1/dsar/export/            { user_email } -> request_id
POST /api/v1/dsar/delete/            { user_email } -> request_id
```

---

# Data model (core entities — high level)

* `User` (id, email, name, password_hash, is_verified, role, created_at)
* `Organization` (id, name, stripe_customer_id, billing_contact, created_at)
* `Plan` (id, name, sku, price_monthly_cents, price_annual_cents, features JSON)
* `Subscription` (id, org_id, plan_id, stripe_sub_id, status, current_period_end)
* `Invoice` (id, org_id, amount_cents, currency, status, pdf_url, stripe_invoice_id)
* `Lead` (id, name, email, company, source, utm, status, owner_id)
* `AuditLog` (id, actor_id, action, target_type, target_id, metadata, created_at)
* `Event` (for product analytics): event_type, payload JSON, created_at

Indexes: `Organization(id)`, `Subscription(org_id)`, `Invoice(org_id)`, `Lead(status)`.

---

# Background jobs & Celery tasks (must-have)

* `process_stripe_webhook` — verify signature, detect event, enqueue specific handler, idempotent.
* `generate_invoice_pdf` — produce PDF and upload to S3; retry with backoff.
* `billing_retry_worker` — dunning strategy; schedule retries and escalate to sales.
* `send_transactional_email` — template-driven email sending (SendGrid/SES).
* `export_dsar_package` — compile PII + activity logs, zip, and provide secure download link.
* `cleanup_temp_files` — housekeeping.

Queue priorities: `webhooks` (high), `emails` (default), `reports` (low).

---

# Design system & UX rules (practical)

* **Theme & fonts:** Inter (primary), system font fallback, font-display:swap.
* **Color tokens:** primary (brand blue), neutral scale, success/warning/danger tokens. Provide accessible contrast token pairs.
* **Spacing tokens:** 4px base scale. 12-column grid, mobile-first.
* **Components:** hero, feature card, pricing card (with accessible toggle), testimonial, integrations grid, FAQ accordion, accessible modal, accessible carousel (if used).
* **Accessibility rules:** keyboard-first navigation, visible focus states, landmarks, semantic headings, alt text for images, ARIA attributes for interactive components. Primary flows must pass automated axe checks and manual keyboard flows.
* **Performance rules:** critical CSS inline for hero; defer noncritical scripts; use modern image formats (AVIF/WebP), responsive images (srcset), and lazy loading for below-the-fold images.

---

# Security & compliance (practical / required)

* TLS 1.2+ enforced site-wide; HSTS enabled.
* Use secure HTTP-only cookies or JWT with refresh token stored in secure cookie.
* CSRF protection for stateful endpoints (Django built-in).
* Input validation & output encoding: prevent SQLi, XSS. Use parameterized ORM queries always.
* Secrets management via environment secrets store (cloud or Vault).
* Access control: RBAC — `superadmin`, `admin`, `sales`, `support`, `user`. Backend enforcement.
* PCI: Do not store card data. Use Stripe Elements/PaymentIntents and tokens.
* PDPA compliance: explicit opt-in for marketing emails, detailed privacy policy, DSAR endpoints, data retention policy (documented), secure deletion procedures. Keep logs for audit trail.
* Penetration test scheduled before GA release.

---

# Testing & QA (concrete)

**Automated**

* Unit tests (Django models, serializers, utilities) — target healthy coverage for critical modules.
* Integration tests for API endpoints (DRF).
* Frontend unit tests (React Testing Library + Jest).
* E2E tests (Cypress) for critical flows: signup, login, trial start, subscription create, invoice download, demo request.

**Accessibility**

* Automated Axe/Lighthouse runs (CI).
* Manual keyboard navigation + screen reader spot checks for primary flows.

**Performance**

* Lighthouse (desktop + mobile) baseline -> track improvements. Set pragmatic launch targets (see next section).

---

# Performance targets (pragmatic)

**Launch (MVP) targets**

* Home (mobile) Lighthouse Performance ≥ 60; Accessibility ≥ 90.
* First Contentful Paint (mobile/4G) ≤ 2.5s initial; aim to reach ≤ 2.0s in first 8 weeks.
* Time To Interactive (TTI) ≤ 4.0s for marketing pages.
  **Rationale:** aggressive >90 right away is ideal but may force scope cut. Use iterative remediation: baseline -> quick wins -> stretch goals.

---

# Accessibility targets

* WCAG 2.1 AA for primary flows: signup, pricing, trial, demo request, invoice retrieval.
* No keyboard traps; focus outlines visible; color contrast passes AA.
* Provide sitemap & skip links for screen readers.

---

# Observability & monitoring (must-have)

* Error tracking: Sentry (tag by org_id).
* Metrics: Prometheus/Grafana or cloud-managed metrics for response times, queue depth, errors.
* Alerts: high error rate, worker queue backlog > threshold, webhook failures > 5%, TLS expiry, disk usage.
* Synthetic monitoring: create transaction checks for `/health`, signup flow, subscription flow.
* Logging: structured JSON logs to central store with PII redaction.

---

# CI/CD & deployment

* Repo: mono-repo or two repos (frontend + backend) — recommend mono-repo for small teams.
* Pipelines: GitHub Actions for linting (ruff/black for Python), unit tests, frontend build, Docker build, deploy to staging.
* Branches: `main` (protected), `develop`, feature branches. Merge via PR with required checks.
* Deploy: staging auto-deploy on `develop`; production deploy via manual promotion from staging with release notes. Support blue/green or canary as infra permits.
* Infrastructure as code: Terraform for cloud infra where practical.

---

# Release plan & phased roadmap (practical timeline)

**Assumptions:** team of 5 (1 PM, 1 Designer, 2 FE devs, 2 BE devs, 1 QA/part-time SRE) — timings adjust with team size.

**Sprint cadence:** 2-week sprints.

**Phase 0 — Prep (week 0)**

* Kickoff, finalize pricing/business rules, baseline Lighthouse report, infra provisioning.

**Phase 1 — Core marketing + lead capture (Sprints 1–3, weeks 1–6)**

* Deliverables: design system, pages (home, features, pricing, contact), lead forms, basic analytics.
* Acceptance: pages live on staging; lead capture verified into DB & CRM webhook.

**Phase 2 — Auth, trial onboarding, billing scaffold (Sprints 4–5, weeks 7–10)**

* Deliverables: auth flows, trial sign-up, Stripe integration scaffold, webhook handler with Celery, invoice generation.
* Acceptance: trial sign-up → subscription record; test Stripe webhook end-to-end (sandbox).

**Phase 3 — Admin, QA, accessibility, performance hardening (Sprints 6–7, weeks 11–14)**

* Deliverables: admin pages, DSAR endpoints, runbooks, monitoring. Hardening & fixes.
* Acceptance: E2E tests pass; critical accessibility issues resolved; monitoring configured.

**Phase 4 — Launch prep & soft launch (Sprint 8, weeks 15–16)**

* Deliverables: production deploy, smoke tests, stakeholder validation, documentation & handover.
* Acceptance: smoke tests green; stakeholders sign off.

---

# Acceptance criteria (pragmatic & testable)

1. **Lead capture**: POST lead form stores lead record with UTM tags; CRM webhook returns 200 and retries are logged on failure.
2. **Signup & trial**: User registers, verifies email, and trial flag set; `trial_started` event appears in analytics within 5 minutes.
3. **Subscription**: Creating subscription returns 201, Stripe webhook processed within 30s, subscription status becomes `active`, invoice PDF accessible.
4. **DSAR**: DSAR export request returns request_id; package delivered within 72 hours (automated task).
5. **Performance**: Home mobile baseline Performance ≥ 60 at launch and Accessibility ≥ 90.
6. **Security**: No high-severity OWASP findings in pre-GA pentest.
7. **Accessibility**: Key flows pass automated axe checks and manual keyboard/screen reader verification.
8. **Monitoring**: Alerts configured for webhook failures and queue backlog; test alert fires and is acknowledged.

---

# Risk register & mitigations (top items)

* **Risk:** Payment/webhook failures cause incorrect billing → revenue loss.
  **Mitigation:** idempotent webhook processing, retries, clear logging & alerting, manual admin override for billing.
* **Risk:** Performance dragged by marketing scripts.
  **Mitigation:** governance on third-party scripts, load third-party tags via GTM server-side or asynchronously.
* **Risk:** PDPA non-compliance or slow DSAR handling.
  **Mitigation:** implement DSAR endpoints early; log processing and SLA; legal sign-off on privacy flow.
* **Risk:** Accessibility failures reduce conversions.
  **Mitigation:** Accessibility checklist for each PR + automated checks + manual testing.

---

# Cost & resourcing (practical estimate)

**One-time (MVP) estimates — SGD (approx.)**

* Design: 8,000
* Frontend dev: 18,000
* Backend dev: 16,000
* QA & PM: 6,000
* DevOps & infra setup: 4,000
* Contingency (15%): 7,350
  **Estimated total (MVP):** **~SGD 59,350**

**Annual run-rate (approx.)**

* Hosting (cloud compute + managed DB): 3,000 – 6,000
* CDN & bandwidth: 600 – 1,200
* Email provider + monitoring (SendGrid, Sentry): 1,200 – 2,400
* Stripe fees (variable): per-transaction
  **Estimated annual OPEX:** **~SGD 5,000 – 10,000+** (depends on traffic and scale)

> Note: these are pragmatic estimates; convert to FTEs & hourly rates per vendor/local market for accuracy.

---

# Sprint backlog (initial — ready to pick up)

**Sprint 1**

* Create repo, linting & CI skeleton, Docker dev images.
* Implement Next.js baseline with home hero + design tokens.
* Setup Django project skeleton + DRF, PostgreSQL & Redis in staging.
* Setup Sentry & basic Prometheus metrics exporter.

**Sprint 2**

* Complete home, features, pricing pages (SSG) + accessible header/footer.
* Implement lead form API and DB model; add UTM capture.
* Implement GA4 server-side event forwarding.

**Sprint 3**

* Auth flows (register/verify/password reset).
* Trial flow UI & backend; `trial_started` event.
* Stripe sandbox account & webhook endpoint with test handler.

**Sprint 4**

* Subscription create UI & API integration with Stripe PaymentIntents.
* Celery + Redis worker deployed; `process_stripe_webhook` implemented.
* Invoice generation skeleton (PDF generation background task).

**Sprint 5**

* Admin views for leads, subscriptions, invoices in Django admin + custom list views.
* DSAR export endpoint prototype & test.
* Accessibility fixes & axe CI integration.

**Sprint 6**

* E2E test suite (Cypress): signup → trial → subscription → invoice download.
* Performance tuning (image optimization, critical CSS).
* Monitoring & alerts finalization.

---

# Governance & RACI (simple)

* **Approve scope & KPIs:** PO (Exec Sponsor) — Responsible
* **Design sign-off:** Designer + Marketing Owner — Responsible / Approver
* **Technical architecture decisions:** Lead Engineer — Responsible; PM & CTO — Consulted
* **Security & PDPA compliance sign-off:** CTO + Legal — Approver
* **Release sign-off:** PM + Lead Engineer — Approver

---

# Deliverables (what you will get at MVP)

* Production-ready Next.js marketing site (English-only) with design system.
* Django 6.0 DRF backend implementing auth, lead capture, subscriptions, invoice generation, DSAR endpoints.
* Celery background workers and Redis queue configuration.
* Stripe integration (sandbox + production-ready webhook handling).
* Admin dashboards (Django admin + lightweight custom pages).
* CI/CD pipelines, monitoring & runbooks.
* API documentation (OpenAPI) and deployment/documentation handover.

---

# Next recommended immediate actions (practical)

1. **Kickoff:** 2-hour stakeholder session to finalize trial rules, PSP decision, and KPI targets.
2. **Baseline audits:** run Lighthouse and accessibility scans on the current site (if any) to set baseline.
3. **Create event taxonomy doc:** finalize the event names and properties for engineering to instrument.
4. **Provision staging infra:** Postgres, Redis, S3, and basic CI pipeline.
5. **Start Sprint 1 tasks** from backlog.

