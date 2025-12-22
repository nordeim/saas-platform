# Project Requirements Document (PRD)

## Project Title
**SaaS Website Redesign for Singapore-Based Medium Enterprise (Full-Stack Implementation)**

---

## Executive Summary

This document defines the refined requirements for a full-stack redesign of a Singapore-based SaaS company's marketing and onboarding website. The solution integrates a modern, conversion-optimized frontend (Next.js 14.2+, React 18, TypeScript) with a robust, scalable backend (Django 6.0+, Django REST Framework, Celery, PostgreSQL 16+, Redis 7.4+). The system will support dynamic content, lead capture, asynchronous tasks, and future extensibility for customer onboarding, analytics, and localization.

---

## 1. Goals & Objectives

### 1.1 Business Goals
- Increase qualified B2B leads by 30% within 6 months
- Improve SEO ranking and organic traffic by 40%
- Reduce bounce rate below 35%
- Enable scalable content management and lead tracking

### 1.2 User Goals
- Understand product value quickly
- Compare pricing tiers and features
- Access documentation, support, and integrations
- Trust the brand through testimonials and case studies

---

## 2. Target Audience

- **Primary**: Product managers, CTOs, and operations leads in mid-sized Southeast Asian businesses
- **Secondary**: Investors, partners, and job seekers

---

## 3. Functional Requirements

### 3.1 Pages & Components

| Page | Key Components |
|------|----------------|
| **Home** | Hero banner, value proposition, CTA, feature highlights, testimonials, partner logos |
| **Features** | Modular feature blocks with icons, illustrations, and use-case narratives |
| **Pricing** | Toggleable pricing table (monthly/annual), feature comparison, CTA buttons |
| **Integrations** | Grid of supported tools with logos, search/filter capability |
| **About Us** | Company mission, leadership bios, milestones, culture |
| **Blog** | CMS-driven articles, categories, search, featured posts |
| **Careers** | Open roles, benefits, culture highlights, application form |
| **Contact** | Form with backend submission to CRM/email, map, contact info |
| **Legal** | Privacy policy, terms of service |

### 3.2 Backend Features (Django + DRF + Celery)

- RESTful API for dynamic content (blog, pricing, integrations, testimonials)
- Admin dashboard (Django Admin) for content management
- Contact form submission → Celery task → Email + CRM webhook
- Blog post scheduling via Django Tasks
- Redis-backed caching for high-traffic endpoints
- Rate limiting and throttling via DRF
- API versioning and schema documentation (drf-spectacular/OpenAPI)

### 3.3 Frontend Features (Next.js 14.2+ + React 18)

- App Router with server components for performance
- Static generation (SSG) for marketing pages
- Incremental Static Regeneration (ISR) for blog and pricing
- Client-side hydration for interactive components (pricing toggles, forms)
- Global state via Zustand or React Context
- SEO meta tags, Open Graph, and structured data
- Responsive design with Mantine UI or Tailwind CSS

---

## 4. Non-Functional Requirements

### 4.1 Performance

- Page load time < 2.5s on 4G
- Lighthouse score > 90 across all categories
- Redis caching for API responses and computed data

### 4.2 Security

- HTTPS enforced with HSTS
- CSRF protection for all forms
- Secure headers via Django middleware
- Rate limiting on API endpoints
- Input validation and sanitization

### 4.3 Maintainability

- Modular codebase with clear separation of concerns
- Environment-based configuration (12-factor app)
- Dockerized development and deployment
- CI/CD with GitHub Actions and staging previews
- Linting (ruff, black, eslint, prettier), type safety (mypy, TypeScript)

---

## 5. Design Requirements

### 5.1 Visual Style

- Clean, whitespace-rich layout inspired by Elementra
- Brand-aligned color palette (Singaporean tech-forward aesthetic)
- Custom illustrations and product mockups
- Consistent iconography and typography (Inter, DM Sans, or similar)

### 5.2 Interaction Design

- Smooth scroll and anchor navigation
- Hover states and microinteractions
- Sticky header with CTA
- Accessible tab/keyboard navigation
- Mobile-first responsive layout

---

## 6. Technical Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14.2+, React 18, TypeScript, Mantine UI or Tailwind CSS |
| **Backend** | Django 6.0+, Django REST Framework, Celery, Django-Q or APScheduler |
| **Database** | PostgreSQL 16+ |
| **Cache/Queue** | Redis 7.4+ |
| **Python** | 3.12+ |
| **Forms** | DRF endpoints + Celery tasks for async processing |
| **CMS** | Django Admin (customized) or headless CMS integration (optional) |
| **Hosting** | Vercel (frontend), Railway/Fly.io/Render (backend) |
| **Monitoring** | Sentry, UptimeRobot, Prometheus (optional) |
| **CI/CD** | GitHub Actions, Docker, Vercel Previews |

---

## 7. Milestones & Timeline

| Phase | Deliverables | Duration |
|-------|--------------|----------|
| **Discovery** | Stakeholder interviews, content audit, analytics review | 1 week |
| **Design** | Wireframes, UI mockups, design system | 2 weeks |
| **Backend Setup** | Django project, DRF scaffolding, Celery, Redis, PostgreSQL schema | 2 weeks |
| **Frontend Development** | Next.js pages, components, API integration | 3 weeks |
| **Testing & QA** | Unit tests, integration tests, Lighthouse, accessibility, security audit | 1 week |
| **Launch** | Production deployment, monitoring setup, post-launch checklist | 1 week |

---

## 8. Success Criteria

- 100% functional coverage of all pages and features
- Lighthouse scores > 90
- Fully responsive and accessible UI
- All CTAs functional and tracked
- Stakeholder sign-off on design and content
- CI/CD pipeline with zero-downtime deploys

---

## 9. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Backend complexity | Use Django Admin for MVP content management |
| Redis/Celery misconfig | Provide Docker Compose with healthchecks and retry policies |
| SEO regression | Pre-launch audit with Screaming Frog + Lighthouse |
| Content delays | Parallelize content creation with design/dev |
| Form spam | Use hCaptcha + rate limiting |

---

## 10. Appendices

- Brand guidelines (to be provided)
- Sitemap diagram (to be created in design phase)
- Component inventory (to be derived from UI audit)
- API schema (to be generated via drf-spectacular)

---

## Next Steps

- Confirm technology stack and CMS preference
- Begin sitemap and wireframe planning
- Define content ownership and delivery schedule
- Set up GitHub repo, CI/CD pipeline, and Dockerized dev environment

