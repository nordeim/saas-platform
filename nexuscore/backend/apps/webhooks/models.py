"""
Webhook models for external service integrations (from PRD-d-3).
"""

import uuid
from django.db import models
from django.utils import timezone


class WebhookEvent(models.Model):
    """Webhook events from external services."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.CharField(max_length=50)  # 'stripe', 'sendgrid', etc.
    event_id = models.CharField(max_length=255, unique=True, db_index=True)
    event_type = models.CharField(max_length=100)
    
    # Raw payload and processed status
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    
    # Retry tracking
    retry_count = models.PositiveIntegerField(default=0)
    last_retry_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'webhook_events'
        indexes = [
            models.Index(fields=['service', 'event_type']),
            models.Index(fields=['processed', 'created_at']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Webhook: {self.service} - {self.event_type}"