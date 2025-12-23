"""
Lead models for marketing and sales tracking (from PRD-d-3).
"""

import uuid
from django.db import models
from django.utils import timezone


class Lead(models.Model):
    """Marketing leads from website forms."""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('disqualified', 'Disqualified'),
    ]
    
    SOURCE_CHOICES = [
        ('website', 'Website Form'),
        ('demo_request', 'Demo Request'),
        ('contact', 'Contact Form'),
        ('event', 'Event'),
        ('referral', 'Referral'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Contact information
    name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=100, blank=True, default='')
    
    # Lead details
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True)
    
    # UTM tracking
    utm_source = models.CharField(max_length=100, blank=True, default='')
    utm_medium = models.CharField(max_length=100, blank=True, default='')
    utm_campaign = models.CharField(max_length=100, blank=True, default='')
    utm_term = models.CharField(max_length=100, blank=True, default='')
    utm_content = models.CharField(max_length=100, blank=True, default='')
    
    # Form data
    form_data = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Conversion tracking
    converted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'leads'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['source', 'created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    
    @property
    def days_since_created(self):
        """Days since lead was created."""
        delta = timezone.now() - self.created_at
        return delta.days
    
    @property
    def full_utm_data(self):
        """Return complete UTM data as dict."""
        return {
            'source': self.utm_source,
            'medium': self.utm_medium,
            'campaign': self.utm_campaign,
            'term': self.utm_term,
            'content': self.utm_content,
        }