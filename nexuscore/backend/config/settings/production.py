"""
Django settings for production environment.
"""

from .base import *

# Security settings for production
DEBUG = False

# Enforce HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS settings for production
CORS_ALLOWED_ORIGINS = get_env_variable('CORS_ALLOWED_ORIGINS').split(',')
CORS_ALLOW_CREDENTIALS = True

# CSRF settings for production
CSRF_TRUSTED_ORIGINS = get_env_variable('CSRF_TRUSTED_ORIGINS').split(',')

# Logging configuration for production
LOGGING['handlers']['file']['level'] = 'ERROR'
LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',
    'class': 'sentry_sdk.integrations.logging.EventHandler',
}
LOGGING['loggers']['django']['handlers'] = ['file', 'sentry']
LOGGING['loggers']['nexuscore']['handlers'] = ['file', 'sentry']

# Sentry configuration
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT,
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=SENTRY_PROFILES_SAMPLE_RATE,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        send_default_pii=False,
    )

# Celery configuration for production
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Cache configuration for production
CACHES['default']['OPTIONS']['CONNECTION_POOL_KWARGS']['max_connections'] = 100

# Disable debug toolbar and silk
DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda request: False}

# Feature flags for production
FEATURE_PAYNOW_ENABLED = get_env_variable('FEATURE_PAYNOW_ENABLED', 'True').lower() == 'true'
FEATURE_DEMO_MODE = get_env_variable('FEATURE_DEMO_MODE', 'False').lower() == 'true'