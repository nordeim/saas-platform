# Canonical PRD — TechFlow Solutions (Merged & Finalized)
**Version 1.1 — Merged PRD**  
**Target launch:** 12–16 weeks (MVP)  
**Stacks:** Django 6.x + DRF + Celery (django-celery-beat) | Next.js 14.2+ + React 18 + TypeScript | PostgreSQL 16+ | Redis 7.4+ | Python 3.12+

> This document merges the operational depth in your original PRD (PRD-o.md) with the pragmatic engineering guidance and safeguards described earlier. Source reference: original PRD sections and artifacts. :contentReference[oaicite:0]{index=0}

---

# 0 — Executive summary
Build a production-grade, Singapore-focused SaaS website + customer portal that combines high-converting marketing pages with a robust app shell and admin tools. Deliverables include: fast public marketing site, secure onboarding & billing (Stripe), a scalable dashboard (analytics, usage, API keys), background processing for heavy work, and operational readiness (monitoring, CI/CD, infra IaC).

Primary objectives (aligned & harmonized with your PRD): increase conversions, reduce time-to-value, sub-2s public page loads (APAC median), API p95 ≤ 200ms, PDPA-compliant operations, and scale to enterprise usage. :contentReference[oaicite:1]{index=1}

---

# 1 — Goals & success metrics (unified)
**Business**
- +15% visitor→trial conversion (3 months post-launch). :contentReference[oaicite:2]{index=2}  
- Trial → paid conversion 5–8% (30 days).

**Performance & Reliability**
- Marketing: LCP ≤ 1.8s (APAC median) and Lighthouse Perf ≥ 90 on CI spot-checks.  
- App API: p95 ≤ 200ms for core endpoints under normal load.  
- Uptime: Marketing site 99.95%; Core app 99.9%.

**Security & Compliance**
- PDPA compliance at GA; evidence matrix for ISO/SOC/PCI readiness (roadmap). :contentReference[oaicite:3]{index=3}

**Operational**
- Background jobs success rate ≥ 99.5% (retries & DLQ handled).
- CI green build and smoke tests required for deploy.

---

# 2 — Scope (MVP vs v1)
**MVP (12–16 weeks)** — Marketing site (hero, features, pricing, testimonials, FAQ), Signup & auth (email+magic link+SSO basic), Trial provisioning, Stripe billing + webhooks, Basic dashboard (usage overview + billing center), Background workers for emails & webhook processing, Admin portal (user & billing ops), Observability (Sentry + Prometheus + Grafana + Loki).

**v1+ (post-MVP)** — Multi-language full support, integration marketplace, advanced analytics, partner portal, multi-tenant DB sharding (if required), formal compliance audits (ISO/SOC). The original PRD already lists broader features; these will be phased. :contentReference[oaicite:4]{index=4}

---

# 3 — Key decisions (short decision log)
1. **Task scheduler:** *Celery 5.5+ + django-celery-beat* as canonical choice for background jobs & scheduling (avoid running parallel schedulers like Django-Q unless a specific feature forces it). Rationale: Celery is robust, widely supported with Redis broker compatibility under Python 3.12. (See Section 6: Background jobs & scheduler).  
   *Source note:* original PRD included Django-Q; we standardize to Celery to reduce ops complexity. :contentReference[oaicite:5]{index=5}

2. **API edge:** Use standard ingress + CDN for most traffic; adopt **Kong API Gateway** only if we require advanced API monetization, fine-grained policy enforcement, or partner routing. (Kong is present in original architecture; keep it as optional). :contentReference[oaicite:6]{index=6}

3. **Observability stack:** Balanced default — *Prometheus + Grafana + Loki + Sentry + OpenTelemetry*. Elastic/ELK remains an option if deep log search or existing licensing justifies it. :contentReference[oaicite:7]{index=7}

4. **Infra model:** Containerized apps deployed to Kubernetes (EKS/GKE) with Terraform IaC; use managed RDS Postgres + ElastiCache Redis for production.

---

# 4 — Architecture (logical)
- **Frontend:** Next.js 14.2+ (App Router) — SSR/ISR for marketing, client components for dashboard; TypeScript, Tailwind, shadcn/ui optional. :contentReference[oaicite:8]{index=8}  
- **Backend:** Django 6.x + DRF serving REST endpoints and admin.  
- **Workers:** Celery workers (Redis broker) + django-celery-beat for scheduled tasks. :contentReference[oaicite:9]{index=9}  
- **DB:** PostgreSQL 16 primary + read replicas.  
- **Cache/Broker:** Redis 7.4+ (cache & Celery broker). :contentReference[oaicite:10]{index=10}  
- **Storage & CDN:** S3-compatible object store + CloudFront/Cloudflare CDN.  
- **Observability:** Prometheus & Grafana (metrics), Loki (logs), OpenTelemetry tracing, Sentry for errors/e2e traces.  
- **Edge / API Gateway:** CDN + ingress; optional Kong for API management. :contentReference[oaicite:11]{index=11}

---

# 5 — Core functional requirements (high level)
**Public marketing**
- Hero, feature grid, pricing (monthly/annual toggle in SGD), testimonials, FAQ, integrations, ROI calculator, resource center, A/B testing hooks (Experiment flagging).

**Auth & onboarding**
- Email verification, password reset, magic links, optional SSO (Google), RBAC (Admin/OrgAdmin/User). Audit logs for critical actions.

**Billing**
- Stripe integration (checkout, subscriptions, promo codes, invoices) + webhook handler that enqueues events for processing. Ensure idempotency and reconciliation job. :contentReference[oaicite:12]{index=12}

**Dashboard**
- Usage overview widget, billing summary, API keys management, integrations panel, exportable reports, settings & team management.

**Admin**
- User management, billing overrides, audit logs, impersonation (admin-only), health & operational dashboards.

**APIs**
- Versioned REST API (v1...), OpenAPI docs via drf-spectacular, rate-limiting, API keys + scoped access.

---

# 6 — Background jobs & scheduler (detailed)
**Chosen approach:** Celery 5.5+ with Redis 7.4 as broker, results either Redis or Postgres depending on durability needs. Use `django-celery-beat` for schedule persistence.

**Job categories**
- Transactional emails & notifications (SendGrid/Twilio)
- Stripe webhook processing & reconciliation
- Scheduled reports & exports
- CSV imports / heavy ETL
- Webhook retry logic / DLQ handling

**Operational controls**
- Worker autoscaling (k8s HPA based on queue length)
- DLQ for failing tasks; alerting on retry thresholds
- Idempotency keys for external events (Stripe)
- Visibility: task metrics exported to Prometheus

**Reason to standardize on Celery:** avoids dual-scheduler complexity present in original PRD (which includes Django-Q). Unifying reduces operator burden and standardizes retry semantics. :contentReference[oaicite:13]{index=13}

---

# 7 — Dependency compatibility matrix (must-ship)
> Run compatibility tests in CI for the following core matrix before locking versions.

| Component | Recommended Version | Notes / Compatibility |
|---|---:|---|
| Python | 3.12.x | Django 6 requires 3.12; pin pip resolver. |
| Django | 6.0.x | Confirm third-party package compatibility. |
| Django REST Framework | 3.15+ | drf-spectacular integration. |
| Celery | 5.5+ | Compatible with Python 3.12; test broker semantics with Redis 7.4. |
| django-celery-beat | latest stable | Persisted schedule for CRON-like tasks. |
| PostgreSQL | 16+ | Use features gradually; run migration checks. |
| Redis | 7.4+ | Broker & cache; test memory policy and AOF/RDB. |
| Next.js | 14.2+ | App Router + TypeScript guidance. |
| React | 18.x | Concurrent features supported. |
| TypeScript | 5.x | Ensure Next.js types alignment. |
| Tailwind CSS | 3.4+ | Design tokens & shadcn/ui recommended. |

**CI Compatibility Tests (mandatory)**
- Nightly matrix builds that run unit tests across Python 3.12 & Django 6, plus Next.js test on Node 20. Run smoke integration tests with ephemeral Postgres/Redis containers.

---

# 8 — Performance SLOs (marketing vs app split)
**Marketing site (public)**  
- LCP ≤ 1.8s (APAC median).  
- Lighthouse Perf ≥ 90 for baseline CI checks.  
- CDN + image optimization + ISR & edge caching required.

**App (authenticated API)**  
- API p95 ≤ 200ms across core endpoints (usage, auth, billing).  
- DB query p95 ≤ 50ms (critical queries).  
- Background job success ≥ 99.5% with retry & DLQ.

**Monitoring & testing**  
- RUM instrumentation for front-end (edge/user RUM).  
- Synthetic checks and load tests (k6/locust) for p95 measurements before production deploy.

---

# 9 — Testing & QA plan (practical, prioritized)
**Testing pyramid**
1. **Unit tests:** Backend (pytest), Frontend (Jest + React Testing Library) — run on PRs.  
   - Target: meaningful coverage on core modules (70–85% where critical).
2. **Integration tests:** DRF endpoints, Celery tasks, Stripe webhooks in staging with test fixtures.  
3. **E2E / Smoke tests:** Playwright for critical flows — *lock these flows*:
   - Signup → verify email → trial provisioning
   - Trial upgrade → Stripe checkout → webhook reconciliation
   - Password reset + SSO login
   - CSV import flow (sample file)
   - Admin impersonation & billing override
   Run in CI as gated checks; full E2E suite nightly. :contentReference[oaicite:14]{index=14}
4. **Performance tests:** k6 or Locust load tests for baseline; keep tests in CI for release candidates.
5. **Security tests:** SAST & dependency SCA on PR; periodic pentest pre-GA.  
6. **Accessibility tests:** axe-core automated audits in CI + manual keyboard/screen-reader checks pre-GA. :contentReference[oaicite:15]{index=15}

**Acceptance tests (must-pass before production)**
- Playwright scenario: Signup → trial provision success (green).  
- Stripe webhook queueing & DB state consistent within 10s in 95% runs.  
- Lighthouse perf checks for marketing page (baseline thresholds).  
- Security SCA issues resolved (no critical).

---

# 10 — Data model (core entities, high level)
- **User**: id, email, hashed_password, role, org_id, last_login, mfa_enabled  
- **Organization**: id, name, stripe_customer_id, plan_id, trial_expires_at, billing_contact  
- **SubscriptionPlan**: id, slug, name, price_monthly_sgd, price_annual_sgd, features_json  
- **Subscription**: id, org_id, stripe_subscription_id, status, current_period_end  
- **UsageRecord**: id, org_id, metric, value, period_start, period_end  
- **APIKey**: id, org_id, key_hash, scopes, created_at, revoked_at  
- **AuditLog**: id, user_id, org_id, action, meta_json, created_at

(Design notes: keep analytics/telemetry in separate time-series or warehouse schema for heavy queries; use read replicas for analytics.) :contentReference[oaicite:16]{index=16}

---

# 11 — Security & compliance (practical)
**Minimum GA controls**
- TLS 1.3+, HSTS, CSP, X-Frame-Options, secure cookies.  
- RBAC & MFA options, account lockout thresholds.  
- Stripe PCI scope minimization (use hosted checkout & minimal card handling).  
- PDPA controls: consent capture, data deletion workflows, PII masking in non-prod. :contentReference[oaicite:17]{index=17}

**Compliance roadmap**
- Create a compliance matrix (control → evidence → owner → target date). Owner assignment required in week 0.

---

# 12 — CI/CD & infra (practical)
**CI (PR gates)**
- Lint, unit tests, fast integration checks, SCA & secret scanning.  
- Playwright smoke tests for protected branches.

**CD**
- Image build → staging canary → promote to prod after automated smoke checks.  
- Infrastructure as Code: Terraform modules (network, k8s, rds, redis, iam). Reuse modules between staging & prod.

**Deployment model**
- Kubernetes (EKS/GKE) + managed Postgres + ElastiCache Redis. Prefer managed for ops savings. Use S3 + CloudFront/Cloudflare for assets.

**Secrets & config**
- Use HashiCorp Vault or cloud-managed secrets (AWS Secrets Manager) and ensure secrets never in code.

---

# 13 — Roadmap & milestones (recommended)
**Week 0 — Discovery & infra**
- Approve PRD (this doc) & owners, provision dev infra, initialize repos, CI skeleton.

**Weeks 1–4 — Foundation**
- Backend skeleton: auth, org model, Stripe sandbox hooks, DRF endpoints for core objects.
- Frontend skeleton: Next.js layout, marketing pages (hero + pricing), auth flows wired to backend sandbox.
- Celery worker & beat baseline + Redis.

**Weeks 5–8 — Core product**
- Dashboard first-value widgets, billing center, admin portal basics, observability instrumentation, E2E smoke tests.

**Weeks 9–12 — Polish & GA prep**
- Performance tuning, accessibility fixes, security hardening, documentation & runbooks, beta launch.

(Adjust timelines per team size and parallelization; original PRD has a similar gantt timeline to reconcile with). :contentReference[oaicite:18]{index=18}

---

# 14 — Risks & mitigations (top)
1. **Dependency incompatibility (Django6 + Py3.12)** — *Mitigation:* nightly compatibility CI matrix; lock safe versions; vendor patch if necessary. :contentReference[oaicite:19]{index=19}  
2. **Webhook storm (Stripe)** — *Mitigation:* queue webhooks in Celery, idempotency logic, backlog scaling & DLQ. :contentReference[oaicite:20]{index=20}  
3. **Performance shortfall for marketing page** — *Mitigation:* implement CDN, image optimization, critical css, ISR for static sections. :contentReference[oaicite:21]{index=21}  
4. **Operational complexity with dual schedulers/gateways** — *Mitigation:* adopt single scheduler (Celery) and optional gateway (Kong only if required). 

---

# 15 — Acceptance criteria (concrete)
- Marketing page: LCP ≤ 1.8s (APAC median) and Lighthouse Perf ≥ 90 on release candidate.  
- Core signup flow: Playwright E2E passes (signup→trial) in staging with 95% success over 10 runs.  
- Stripe: webhook processed with DB update within 10s for 95% of synthetic events.  
- Observability: critical dashboards present (SLA, worker health, error rate) and alerts configured.  
- Security: SCA raises zero critical vulnerabilities; Snyk/Dependabot processes in place.

---

# 16 — Deliverables & next steps (immediate)
Choose one to start and I will produce it immediately:

1. **Merged PRD (this doc)** — approved; next produce: *detailed implementation plan* (week-by-week tasks + GitHub milestones + owners).  
2. **Skeleton repo** — monorepo template with Next.js + Django + DRF + Celery + GitHub Actions CI & Terraform skeleton.  
3. **Compliance & evidence matrix** — assign owners and generate required artifacts checklist for PDPA/PCI/ISO.  
4. **Test & release playbook** — Playwright scripts for critical flows, k6 load test harness, and CI test matrix.

If you confirm, I will proceed with choice **(2) Skeleton repo** or **(1) Detailed implementation plan** (recommended first).  

---

# Appendix — Source reconciliation
- Original PRD (uploaded) provided detailed UX design tokens, breakpoints, Gantt timeline, and extensive infra examples; this canonical PRD consolidates those items and standardizes operational choices (notably Celery + django-celery-beat vs Django-Q, and a split SLO approach for marketing vs app shell). See original artifact for full component-level detail. :contentReference[oaicite:23]{index=23}

