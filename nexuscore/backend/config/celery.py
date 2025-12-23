import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('nexuscore')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure task routing
app.conf.task_routes = {
    'apps.webhooks.tasks.process_stripe_webhook': {'queue': 'high'},
    'apps.billing.tasks.generate_invoice_pdf': {'queue': 'default'},
    'apps.privacy.tasks.enforce_pdpa_retention': {'queue': 'low'},
    'apps.billing.tasks.send_dunning_emails': {'queue': 'low'},
}

# Task configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Singapore',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)