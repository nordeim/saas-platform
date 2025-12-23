# NexusCore v4.0 - Singapore B2B SaaS Platform

A production-ready B2B SaaS platform built with Django 6.0 and Next.js, featuring Singapore GST compliance, PDPA automation, and enterprise-grade security.

## 🎯 Features

### Singapore Compliance ✨
- **GST Calculation**: Database-level GST calculation using Django 6.0 GeneratedField
- **UEN Validation**: ACRA-compliant UEN format validation
- **IRAS Transaction Codes**: E-invoicing compliance with SR/ZR/OS/TX codes
- **PDPA Automation**: Automated data retention with differential policies (2yr/7yr)

### Enterprise Infrastructure 🏗️
- **Idempotency**: Complete duplicate prevention framework
- **Payment Processing**: Stripe integration with PayNow support
- **Monitoring**: Comprehensive observability with Prometheus/Grafana
- **Security**: Django 6.0 native CSP, rate limiting, and security headers

### Technical Stack 🚀
- **Backend**: Django 6.0 + PostgreSQL 16 + Redis 7.4
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Task Queue**: Celery 5.x with Redis broker
- **Deployment**: Docker + AWS ap-southeast-1 (Singapore region)

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 16
- Redis 7.4
- Docker & Docker Compose

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd nexuscore

# Copy environment template
cp .env.template .env

# Edit environment variables
nano .env
```

### 2. Start with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Load initial data (optional)
docker-compose exec backend python manage.py loaddata initial_data
```

### 3. Access the Application

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs

## 📁 Project Structure

```
nexuscore/
├── backend/                    # Django backend
│   ├── apps/
│   │   ├── core/              # Core functionality
│   │   ├── users/             # User management
│   │   ├── organizations/     # Organization management
│   │   ├── billing/           # Billing & GST compliance
│   │   ├── subscriptions/     # Subscription management
│   │   ├── privacy/           # PDPA compliance
│   │   ├── leads/             # Lead management
│   │   ├── webhooks/          # External integrations
│   │   └── events/            # Analytics & auditing
│   ├── config/
│   │   ├── settings/          # Django settings
│   │   ├── urls.py           # URL configuration
│   │   └── wsgi.py           # WSGI application
│   ├── requirements/          # Python dependencies
│   ├── templates/            # Django templates
│   ├── static/               # Static files
│   ├── logs/                 # Application logs
│   ├── Dockerfile            # Backend container
│   └── manage.py             # Django management
│
├── frontend/                 # Next.js frontend
│   ├── app/                  # App directory (Next.js 14)
│   ├── components/           # React components
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utility functions
│   ├── public/               # Static assets
│   ├── styles/               # Global styles
│   ├── Dockerfile            # Frontend container
│   ├── next.config.js        # Next.js configuration
│   └── tailwind.config.js    # Tailwind CSS config
│
├── nginx/                    # Nginx configuration
│   └── nginx.conf
│
├── docker-compose.yml        # Docker Compose setup
├── .env.template             # Environment template
└── README.md                 # This file
```

## 🔧 Environment Configuration

Copy `.env.template` to `.env` and configure the following:

### Database
```bash
DB_NAME=nexuscore
DB_USER=nexuscore_user
DB_PASSWORD=your-secure-password
```

### Stripe (for payments)
```bash
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=pk_test_your_key
```

### AWS S3 (Singapore region required)
```bash
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=nexuscore-storage
AWS_S3_REGION_NAME=ap-southeast-1  # Singapore data residency
```

### SendGrid (for emails)
```bash
EMAIL_HOST_USER=your-username
EMAIL_HOST_PASSWORD=your-password
```

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=apps

# Run specific app tests
docker-compose exec backend pytest apps/billing/tests/
```

### Frontend Tests

```bash
# Unit tests
cd frontend && npm test

# E2E tests with Cypress
cd frontend && npm run cypress
```

## 📊 Monitoring & Observability

### Application Metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)
- **Sentry**: Error tracking (configure DSN)

### Health Checks
- **Backend Health**: http://localhost:8000/health/
- **Readiness Check**: http://localhost:8000/ready/

## 🔒 Security Features

### Django 6.0 Security
- ✅ Native CSP support with nonce generation
- ✅ Connection health checks for database reliability
- ✅ Modern email API with Unicode support
- ✅ Async view patterns for high-concurrency operations

### Application Security
- ✅ Idempotency framework preventing duplicate payments
- ✅ Rate limiting on authentication endpoints
- ✅ Security headers (HSTS, CSP, XSS protection)
- ✅ Input validation and sanitization

### Compliance Security
- ✅ PDPA data retention automation
- ✅ Manual approval required for data deletion
- ✅ Audit trail for all user actions
- ✅ Singapore data residency (AWS ap-southeast-1)

## 📈 Performance

### Database Optimization
- ✅ PostgreSQL 16 with connection pooling
- ✅ GeneratedField for GST calculations (database-level)
- ✅ Optimized indexes for common queries
- ✅ Partial indexes for specific conditions

### Application Optimization
- ✅ Django 6.0 async views
- ✅ Redis caching with connection pooling
- ✅ Celery task queue with priority routing
- ✅ Static file optimization with CDN

### Frontend Optimization
- ✅ Next.js 14 with App Router
- ✅ Image optimization with WebP support
- ✅ Tailwind CSS with PurgeCSS
- ✅ Code splitting and lazy loading

## 🌏 Singapore-Specific Features

### GST Compliance
```python
# Database-level GST calculation
gst_amount_cents = models.GeneratedField(
    expression=models.Func(
        models.F('subtotal_cents') * models.F('gst_rate'),
        function='ROUND',
        output_field=models.BigIntegerField()
    ),
    output_field=models.BigIntegerField(),
    db_persist=True
)
```

### UEN Validation
```python
uen = models.CharField(
    max_length=15,
    validators=[
        RegexValidator(
            regex=r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$',
            message="Enter a valid Singapore UEN."
        )
    ]
)
```

### PDPA Automation
```python
@shared_task
def enforce_pdpa_retention():
    # Marketing data: 2 years
    # Financial data: 7 years (IRAS)
    # User data: 2 years (unless financial data exists)
```

## 🚀 Deployment

### Production Deployment

```bash
# Set production environment
export DJANGO_SETTINGS_MODULE=config.settings.production

# Build production images
docker-compose -f docker-compose.prod.yml build

# Run migrations
docker-compose -f docker-compose.prod.yml run backend python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml run backend python manage.py collectstatic --noinput

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

### AWS Deployment

1. **EC2**: Application servers in ap-southeast-1
2. **RDS**: PostgreSQL 16 with Multi-AZ
3. **ElastiCache**: Redis cluster for caching
4. **S3**: Static files and media storage
5. **CloudFront**: CDN for global distribution
6. **Route 53**: DNS management
7. **ACM**: SSL certificate management

## 📖 Documentation

### API Documentation
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

### Code Documentation
- **Python Docstrings**: Comprehensive documentation
- **Type Hints**: Full type annotation support
- **Architecture Docs**: C4 model diagrams

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.nexuscore.sg](https://docs.nexuscore.sg)
- **Issues**: [GitHub Issues](https://github.com/nexuscore/nexuscore/issues)
- **Email**: support@nexuscore.sg
- **Phone**: +65 6123 4567

---

**Built with ❤️ in Singapore**  
*Empowering businesses with compliant, scalable SaaS solutions*