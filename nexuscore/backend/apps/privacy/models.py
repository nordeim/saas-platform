"""
Privacy and PDPA compliance models for NexusCore.
"""

import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.users.models import User


class DSARRequest(models.Model):
    """Data Subject Access Request tracking for PDPA compliance."""
    
    REQUEST_TYPE_CHOICES = [
        ('export', 'Data Export'),
        ('delete', 'Data Deletion'),
        ('access', 'Data Access'),
        ('rectification', 'Data Rectification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verifying', 'Verifying Identity'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Requester information
    user_email = models.EmailField(db_index=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='dsar_requests'
    )
    
    # Request details
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Verification
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_method = models.CharField(max_length=50, blank=True)
    
    # Processing
    export_url = models.URLField(blank=True)
    export_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    failure_reason = models.TextField(blank=True)
    
    # Timestamps with SLA tracking
    requested_at = models.DateTimeField(auto_now_add=True)
    processing_started_at = models.DateTimeField(null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Manual approval for deletions (PDPA requirement) [CRITICAL]
    deletion_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_dsar_deletions'
    )
    deletion_approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'dsar_requests'
        indexes = [
            models.Index(fields=['user_email']),
            models.Index(fields=['status', 'requested_at']),
            models.Index(fields=['request_type', 'status']),
            models.Index(fields=['requested_at']),
            # Partial index for pending requests (SLA monitoring)
            models.Index(
                fields=['status'],
                condition=models.Q(status='pending'),
                name='idx_pending_dsar'
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(status='completed') | models.Q(processed_at__isnull=False),
                name='completed_dsar_requires_processed_at'
            ),
            models.CheckConstraint(
                check=~models.Q(request_type='delete') | models.Q(deletion_approved_by__isnull=False),
                name='deletion_requires_approval'
            ),
        ]
    
    def __str__(self):
        return f"DSAR {self.id} - {self.user_email} ({self.request_type})"
    
    @property
    def sla_status(self):
        """Check if request is within 72-hour SLA."""
        if self.status == 'completed':
            return 'completed'
        
        hours_since_request = (timezone.now() - self.requested_at).total_seconds() / 3600
        
        if hours_since_request < 48:
            return 'within_sla'
        elif hours_since_request < 72:
            return 'approaching_sla'
        else:
            return 'breached_sla'
    
    @property
    def hours_remaining_in_sla(self):
        """Hours remaining in 72-hour SLA."""
        hours_elapsed = (timezone.now() - self.requested_at).total_seconds() / 3600
        return max(0, 72 - hours_elapsed)
    
    def clean(self):
        """Validate DSAR data."""
        if self.export_expires_at and self.export_expires_at <= timezone.now():
            raise ValidationError({
                'export_expires_at': 'Export expiry must be in the future.'
            })
        
        if self.processed_at and self.processed_at < self.requested_at:
            raise ValidationError({
                'processed_at': 'Processed date cannot be before request date.'
            })
        
        super().clean()