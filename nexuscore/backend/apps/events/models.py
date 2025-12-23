"""
Event models for analytics and auditing (from PRD-d-3).
"""

import uuid
from django.db import models
from django.utils import timezone

from apps.users.models import User
from apps.organizations.models import Organization


class Event(models.Model):
    """System events for analytics and auditing."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'events'
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['organization', 'created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Event: {self.event_type} - {self.created_at}"