# Project Requirements Document (PRD)
**Project:** SaaS Marketing & Product Website (Singapore — Medium SaaS company)  
**Based on:** UI/UX cues from Elementra SaaS theme  
**Primary Tech Stack:**  
- **Backend:** Django 6.x, Django REST Framework (DRF), Celery, Django Tasks  
- **Frontend:** Next.js 14.2+, React 18, TypeScript  
- **DB / Cache:** PostgreSQL 16+, Redis 7.4+  
- **Python:** 3.12+  

---

# 1. Executive summary
Build a production-ready marketing + product website for a Singapore-based medium SaaS company that: (1) converts visitors into trial/demo signups and leads, (2) clearly explains product capabilities (including billing, basic accounting/inventory modules), and (3) supports a single-page, component-driven UX inspired by the Elementra SaaS theme. The site will be headless: Next.js frontend consuming DRF APIs, and it will include an admin area / CMS for content, subscription management and background jobs for billing/reporting.

**Primary objectives**
- Clear product positioning, pricing, and CTAs (free trial/demo request).
- Reliable signup + subscription flow integrated with payments.
- Reusable component system and SEO-first pages.
- Production-grade non-functional requirements: security, accessibility (WCAG AA target), performance, observability, and PDPA compliance for Singapore.

---

# 2. Stakeholders & users
**Primary stakeholders**
- Product Owner / CEO
- Head of Marketing
- CTO / Engineering Lead
- Sales & Customer Success

**User personas**
- Product Decision Maker (PM/Director): wants features, pricing, ROI.
- Technical Buyer (DevOps/IT Manager): wants integrations, API docs, security info.
- End-user (Operations/Admin): wants simple onboarding, tutorials.
- Sales/CS team: needs admin tools to manage leads, trials, and subscriptions.

---

# 3. Scope (what's in / out)
**In scope**
- Marketing pages (home, features, pricing, integrations, docs, blog, contact, FAQ)
- Auth: sign-up / login / password reset / email verification
- Subscription management (Stripe or PSP integration)
- Free trial and paid plans (billing toggles: monthly/annual)
- Lead capture (forms, newsletter)
- Basic built-in features demo pages: accounting-lite (invoicing), inventory-lite (product + stock), dashboards (read-only mockup)
- Admin dashboard: users, customers, plans, invoices, content management
- Background jobs (billing, emails, periodic reports)
- Analytics events & instrumentation
- Accessibility and SEO optimizations
- CI/CD pipelines, monitoring & alerting

**Out of scope (initial release)**
- Full ERP capabilities (complex accounting, tax jurisdictions beyond Singapore)
- Custom enterprise SSO beyond OAuth/SAML (can be planned later)
- Multi-tenant product customizations per customer (single product instance with org scope)

---

# 4. High-level user journeys
1. Visitor lands on Home → reads hero/benefits → explores pricing → starts free trial → signs up → verifies email → enters billing (if required) → accesses product/dashboard.
2. Visitor reads Features / Integrations → requests demo → Sales receives lead → schedules demo.
3. Admin logs into dashboard → views subscriptions, invoices, trigger refunds, export CSV.
4. System sends monthly/annual invoices, payment retries handled via background jobs.

---

# 5. Functional requirements

## 5.1 Marketing & Content
- CMS-managed pages (title, hero, sections, CTA, meta tags) via Django admin + simple content models or headless CMS (optional).
- SEO meta management (title, description, open graph, canonical).
- Blog with markdown support and RSS feed.
- Static exports for selected pages (Next.js ISR) for speed and SEO.

## 5.2 Authentication & Authorization
- Email/password auth + email verification; password reset via secure tokens.
- Optional social login (Google, GitHub).
- RBAC: roles = [superadmin, admin, sales, support, user]. Authorization enforced server-side.
- JWT-based session for API (short-lived access tokens + refresh tokens) OR secure cookie sessions depending on security policy.

## 5.3 Subscription & Billing
- Plans: free trial, starter, pro, enterprise (configurable in admin).
- Payment provider integration (Stripe recommended). Support currency SGD and at least one major international currency.
- Billing toggles (monthly/annual) with proration rules for mid-cycle plan change.
- Invoicing: generate PDF invoices, store invoices in DB, email invoices to customers.
- Webhooks support (payment succeeded, failed, dispute) and webhook processing via Celery tasks.
- Payment retry logic and dunning notifications.

## 5.4 Demo / Trial / Lead capture
- Forms with reCAPTCHA (or hCaptcha), server-side validation, UTM capture, and CRM export (CSV or webhook).
- Lead scoring fields and sales notifications via email / Slack integration.

## 5.5 Product demo features (read-only)
- Simple dashboard mock-ups showing analytics, team activity, and sample accounting/inventory screens.
- Demo dataset seeded for each demo account.

## 5.6 Admin & Operations
- Admin UI to manage users, organizations, subscriptions, invoices, content.
- Export capabilities (CSV for customers, invoices).
- Audit logs for critical operations (billing changes, refunds, role changes).

## 5.7 Integrations
- Payment gateway (Stripe)
- Webhooks to CRM (HubSpot/SendGrid/optional)
- Email provider (SendGrid/Mailgun or AWS SES)
- Optional accounting integrations (Xero/QuickBooks) as future scope (webhooks + API connectors)

---

# 6. Non-functional requirements (NFRs)

## 6.1 Security
- OWASP Top 10 hardening in code & infra.
- TLS 1.2+ everywhere, HSTS enabled.
- Secrets management (e.g., Vault or cloud secrets).
- Rate limiting: API-level rate limiting with Redis (e.g., 60 req/min default).
- Input validation, sanitization, and parameterized DB queries - ORM usage.
- CSRF protection for stateful endpoints.
- Strong password policy and optional 2FA for admin users.
- PCI compliance guidance: do not store card data; use PSP tokenization.

## 6.2 Performance & Scalability
- Target Lighthouse scores: Performance ≥ 60 (initial), Accessibility ≥ 90, aim to improve iteratively.
- CDN for static assets; images served in modern formats (WebP/AVIF).
- Server-side rendering (SSR) or incremental static regeneration (ISR) for marketing pages to maximize SEO and speed.
- Caching layer: Redis for sessions, rate-limiting, and ephemeral caches. CDN caching for static files and public pages.

## 6.3 Availability & Reliability
- Aim for 99.9% service availability SLA for public marketing pages and authentication services. (Operational SLA to be defined by stakeholders.)
- Health checks and automated restarts.

## 6.4 Accessibility & Internationalization
- WCAG 2.1 AA compliance for primary flows (trial signup, pricing pages).
- Multi-language readiness (i18n) with initial English (Singapore) support. Consider future translations (e.g., Chinese, Malay).

## 6.5 Compliance (Singapore PDPA)
- Explicit consent for marketing communications; clear privacy policy and cookie banner.
- Data retention policy for PII, secure deletion flows, and export capabilities for user data.
- Data residency considerations: note where data stored; ensure provider compliance as necessary.

---

# 7. Architecture & technical design

## 7.1 Logical architecture
- **Frontend (Next.js + TypeScript)**: public site pages, marketing pages, pricing toggles, demo flows, client-side product UI that interacts with API.
- **API (Django + DRF)**: public API endpoints for auth, subscriptions, admin, content, invoice retrieval.
- **Background Workers (Celery)**: process webhooks, send emails, generate invoices, scheduled reports, payment retries.
- **Data stores**: PostgreSQL primary; Redis for cache & Celery broker (or RabbitMQ if preferred).
- **File storage**: S3-compatible storage for asset uploads and invoice PDFs.
- **Third-party services**: Stripe (payments), SendGrid (emails), Sentry (error monitoring), Prometheus/Grafana (metrics), Cloud CDN (fast assets).

## 7.2 Deployment pattern
- Containerized services (Docker) deployed to a cloud provider (managed Kubernetes or App Service). Alternatives: managed Platform-as-a-Service (Heroku, Render) depending on org preference.
- CI/CD: GitHub Actions (or equivalent) to build, run tests, lint, and deploy to staging/production.
- Infrastructure as Code: Terraform for cloud resources.

---

# 8. Data model (high-level)

**Core entities**
- `User` (id, email, full_name, role, last_login, is_active, org_id, created_at)
- `Organization` (id, name, domain, billing_info, stripe_customer_id)
- `Subscription` (id, org_id, plan_id, status, started_at, next_billing_at, stripe_subscription_id)
- `Plan` (id, name, price_monthly, price_annual, features JSON)
- `Invoice` (id, org_id, amount, currency, status, pdf_url, due_date, stripe_invoice_id)
- `Product` (for inventory feature: id, sku, name, description, cost_price, sales_price, stock_level)
- `Order` (id, org_id, product_id, qty, total_amount, status)
- `AuditLog` (user_id, action, resource_type, resource_id, metadata, timestamp)
- `Event` (for analytics: event_type, org_id, user_id, payload, created_at)

**Indexing & partitioning**
- Index by `organization_id` for multi-org queries.
- Audit logs and events can be stored in a separate write-optimized table (or time-series DB) to prevent bloat.

---

# 9. API surface (selected endpoints)

> Note: All API endpoints require HTTPS. Use JSON for payloads except file downloads.

**Auth**
```

POST /api/v1/auth/register/      { email, password, org_name, plan_id? }
POST /api/v1/auth/login/         { email, password } -> { access_token, refresh_token }
POST /api/v1/auth/refresh/       { refresh_token } -> { access_token }
POST /api/v1/auth/verify-email/  { token }
POST /api/v1/auth/password-reset-request/ { email }
POST /api/v1/auth/password-reset/ { token, new_password }

```

**Subscription & Billing**
```

GET  /api/v1/plans/
POST /api/v1/subscriptions/             { org_id, plan_id, payment_method_id }
GET  /api/v1/subscriptions/{id}/
POST /api/v1/subscriptions/{id}/cancel/
POST /api/v1/subscriptions/{id}/change-plan/ { plan_id }
GET  /api/v1/invoices/                  (list)
GET  /api/v1/invoices/{id}/download/    (PDF)

```

**Admin**
```

GET /api/v1/admin/users/
PATCH /api/v1/admin/users/{id}/
POST /api/v1/admin/invoices/{id}/email/

```

**Demo / Product**
```

GET /api/v1/demo/dashboard/
GET /api/v1/products/ (inventory)
POST /api/v1/orders/  { product_id, qty }

```

**Webhooks**
```

POST /api/v1/webhooks/stripe/  (verify signature & enqueue processing)

```

---

# 10. Background jobs & scheduled tasks (Celery)
- `process_stripe_webhook` — handle payment events (invoice.paid, invoice.payment_failed, charge.refund)
- `generate_invoice_pdf` — create PDF for invoices and store to S3
- `billing_retry_job` — retry failed payments per dunning schedule
- `send_email_task` — queued email sending (transactional)
- `daily_reports` — scheduled summary emails for admins (usage, revenue)
- `cleanup_temp_files` — periodic housekeeping
- `export_large_csv` — async CSV generation for admin exports

Queue strategy: dedicated queues (high-priority (webhook/billing), default (emails), low-priority (reports)). Configure retries and exponential backoff.

---

# 11. UX / UI component & design system (front-end spec)
**Core components**
- Hero + CTA (configurable headline, subhead, primary & secondary CTAs)
- Feature cards (icon, title, description)
- Pricing cards (tier badge, price toggle monthly/annual, CTA)
- Integrations grid (logos)
- Testimonial carousel (accessible)
- FAQ accordion (ARIA compliant)
- Newsletter / Contact forms
- Global navigation and footer (with quick links & legal)
- Dashboard components for demo (metrics, charts - use client-side charting like Recharts)

**Style & tokens**
- System fonts (prefer system-ui stack for performance) + scale for H1/H2/H3/body
- Color tokens: primary, secondary, accent, muted, background, success, warning, danger
- Spacing scale (4px base): tokens for small/medium/large paddings
- Focus states: 3px visible outline for keyboard users
- Mobile-first responsive breakpoints: base, sm, md, lg, xl
- Dark mode: optional, plan for later

**Accessibility**
- All interactive components keyboard accessible
- Semantic HTML and landmarks
- Proper alt text for images; decorative images set `aria-hidden`/presentational
- Ensure color contrast >= 4.5:1 for body text and >= 3:1 for large headings

---

# 12. Analytics, instrumentation & SEO
**Events to track**
- `page_view` (with UTM tags)
- `cta_click` (hero, pricing, demo request)
- `plan_selected`
- `trial_started`
- `subscription_created`
- `invoice_viewed`
- `contact_form_submitted`

Analytics stack: GA4 + server-side event forwarding (for critical events), optional product analytics (PostHog/Amplitude).

**SEO**
- SSR/ISR for marketing pages, canonical tags, structured data for FAQ and Organization schema.
- Sitemap.xml and robots.txt generation.
- Meta tags and OG images per page.

---

# 13. Testing & QA
**Automated tests**
- Unit tests (Django): models, serializers, utils
- API integration tests (DRF)
- Frontend unit tests (Jest + React Testing Library)
- E2E tests (Cypress) for critical flows: signup, login, subscription, invoice download

**Manual testing**
- Accessibility audit (axe + manual keyboard navigation)
- Cross-browser and mobile testing on major browsers & devices
- Payment flow test scenarios (successful payment, failed, dispute)

**Acceptance tests**
- Signup + verify email + login flow works end-to-end
- Subscribe to plan, invoice generated & downloadable PDF
- Payment webhook processed and subscription status updated
- Admin CSV export works for 10k records (async)
- Lighthouse baseline collected & reported

---

# 14. Monitoring & Observability
- Error tracking: Sentry (capture exceptions, with tagging by organization)
- Metrics: Prometheus for service metrics; Grafana dashboards for CPU/memory/queue depth/response times
- Logs: structured logs shipped to centralized system (e.g., ELK or cloud log service)
- Alerts: high error rate, worker queue backlog, failed webhook processing, disk usage, TLS expiry
- Uptime monitoring: synthetic checks for critical endpoints (/, /health, /api/v1/auth/health)

---

# 15. CI/CD & release process
- Branch strategy: main (protected), develop, feature/* branches
- PR checks: linters (Black/ruff for Python; ESLint/Prettier for JS), tests, type-check (mypy/TS)
- Deploy: automated deploy to staging on merge to develop; manual gated deploy to production from main (with required approvals)
- Blue/green or canary deployment pattern for backend (if infra available)

---

# 16. Data privacy & PDPA considerations (Singapore)
- Provide explicit consent mechanisms for marketing emails and cookies.
- Implement Data Subject Access Request (DSAR) workflow (export and delete user data).
- Maintain data retention policy: define retention windows for logs and PII, document secure deletion processes.
- Ensure third-party providers (Stripe, SendGrid, cloud provider) have contractual safeguards; document data flow and subprocessors.

---

# 17. Risks & mitigation
- **Risk:** Elementor-inspired asset-heavy design might slow pages.  
  **Mitigation:** Re-implement components in Next.js with optimized assets, lazy loading, and CDN usage.

- **Risk:** Payment edge-cases causing revenue loss.  
  **Mitigation:** Thorough webhook handling, idempotency keys, retry and alerting on failures.

- **Risk:** Poor accessibility impacting conversions and compliance.  
  **Mitigation:** Accessibility-first dev checklist, automated tests, manual audits.

- **Risk:** Scope creep (inventory/accounting feature bloat).  
  **Mitigation:** Ship minimal viable accounting/inventory (invoicing + product stock) with clear boundaries; plan advanced features for later phases.

---

# 18. Acceptance criteria & success metrics
**Must-have acceptance criteria**
- Signup → verified account → access to demo dashboard (end-to-end) passes in staging.
- Subscription flow integrated with PSP; invoices generated and downloadable.
- Marketing pages render via SSR/ISR and pass basic SEO checks (title, meta, OG).
- Automated tests pass in CI; critical E2E tests stable.
- Accessibility: no critical WCAG AA failures on primary flows.
- Monitoring & alerts configured for key failures.

**Success metrics (initial)**
- Trial signup conversion rate (baseline & target to be defined by stakeholders).
- Time-to-first-meaningful-paint improvement vs baseline (measurable via Lighthouse).
- Error rate < 1% for production transactions (monitoring).

> Note: stakeholders should define business-specific KPI targets and measurement windows.

---

# 19. Deliverables (initial release)
- Production-ready Next.js marketing site with component library and accessible components.
- DRF backend implementing auth, subscription, invoice generation, and admin endpoints.
- Celery-based background job pipeline for billing and webhook processing.
- Admin UI for core operations.
- CI/CD pipelines, monitoring dashboards, and runbooks.
- Documentation: API docs (OpenAPI/Swagger), deployment guide, runbook for critical operations (billing failures, DSAR).

---

# 20. Implementation phases & checklists (milestone-based — no timelines)
## Phase A — Discovery & detailed design
- [ ] Confirm product positioning, target plans, and pricing rules with stakeholders.
- [ ] Content inventory and mapping for pages.
- [ ] Finalize integrations (payment provider, email provider).
- [ ] Accessibility & SEO targets agreed.

## Phase B — Core platform & API
- [ ] Bootstrap Django project + DRF; set up PostgreSQL and Redis.
- [ ] Implement auth flows (register/login/email verify/password reset).
- [ ] Implement plans & subscription models; Stripe integration scaffold + webhook handler.
- [ ] Implement invoice generation and PDF storage.

## Phase C — Frontend & design system
- [ ] Create design system (tokens, components).
- [ ] Implement public pages (home, features, pricing) with SSR/ISR.
- [ ] Implement signup & subscription UI and demo dashboard.

## Phase D — Background jobs, admin, and edge flows
- [ ] Celery tasks for webhooks, invoice generation, email sending.
- [ ] Admin pages for user and subscription management.
- [ ] Implement analytics instrumentation and event forwarding.

## Phase E — QA, hardening & launch prep
- [ ] Run full test suite and E2E flows.
- [ ] Perform performance & accessibility audits; address critical issues.
- [ ] Configure monitoring, alerts, and backup procedures.
- [ ] Documentation handover.

## Phase F — Launch & post-launch
- [ ] Soft launch to internal users; monitor metrics & errors.
- [ ] Address post-launch bugs, iterate on performance and conversion tests.
- [ ] Plan next feature set (Xero integration, SSO, multi-language).

---

# 21. Maintenance & operational considerations
- Backup strategy: daily DB backups with point-in-time recovery.
- Patch & dependency management: monthly review of critical dependencies and security patches.
- Incident response playbook: roles, communications, rollback procedure.
- Cost monitoring and performance tuning (to control hosting and CDN costs).

---

# 22. Appendix

## Sample UI content mapping (example)
- Hero: headline, subhead, primary CTA (Start free trial), secondary CTA (Request demo)
- Features: 6 cards (title, short description, icon)
- Pricing: 3 tiers, monthly/annual toggle, FAQ snippet under pricing
- Footer: links, privacy, terms, contact

## Example acceptance tests (technical)
- `test_register_flow_creates_org_and_user()` — asserts DB rows & email token created.
- `test_stripe_webhook_invoice_paid_updates_subscription()` — simulate webhook and assert subscription status.
- `e2e_signup_and_subscribe.cypress` — full end-to-end flow assertion.

---

# 23. Next recommended actions (immediate)
1. Gather stakeholders for a single kickoff: finalize pricing, trial policy (duration, billing capture required or not), PSP choice, and brand assets.  
2. Create a content spreadsheet mapping all placeholder sections to owners and deadlines.  
3. Provision staging infra (Postgres + Redis + S3) and initialize repo with basic CI to enforce quality gates.

---

# Glossary
- **PSP:** Payment Service Provider (e.g., Stripe)  
- **ISR:** Incremental Static Regeneration (Next.js)  
- **PDPA:** Personal Data Protection Act (Singapore)  
- **WCAG:** Web Content Accessibility Guidelines  
- **SLA:** Service Level Agreement

