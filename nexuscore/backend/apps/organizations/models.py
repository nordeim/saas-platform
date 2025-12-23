"""
Organization models for NexusCore with Singapore compliance.
"""

import uuid
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from apps.users.models import User


class Organization(models.Model):
    """Company/Organization entity with Singapore compliance."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    
    # Singapore UEN Validation [CRITICAL]
    uen = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$',
                message="Enter a valid Singapore UEN."
            )
        ],
        help_text="Unique Entity Number (ACRA registered)"
    )
    
    # GST Compliance [CRITICAL]
    is_gst_registered = models.BooleanField(default=False)
    gst_reg_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^M[0-9]{8}[A-Z]{1}$',
            message="Invalid GST registration number format"
        )]
    )
    
    # Billing information
    stripe_customer_id = models.CharField(max_length=255, blank=True, db_index=True)
    billing_email = models.EmailField()
    billing_phone = models.CharField(max_length=20, blank=True, default='')
    billing_address = models.JSONField(default=dict, blank=True)
    
    # Settings
    timezone = models.CharField(max_length=50, default='Asia/Singapore')
    locale = models.CharField(max_length=10, default='en-SG')
    settings = models.JSONField(default=dict, blank=True)
    
    # Relationships
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owned_organizations')
    members = models.ManyToManyField(User, through='OrganizationMembership')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'organizations'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['uen']),  # Critical for UEN lookups
            models.Index(fields=['stripe_customer_id']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(trial_ends_at__gte=models.F('created_at')),
                name='trial_ends_after_creation'
            ),
            models.CheckConstraint(
                check=~models.Q(is_gst_registered=True) | models.Q(gst_reg_no__isnull=False),
                name='valid_gst_registration'
            )
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_trial(self):
        """Check if organization is in trial period."""
        if not self.trial_ends_at:
            return False
        return timezone.now() < self.trial_ends_at
    
    @property
    def days_left_in_trial(self):
        """Days remaining in trial."""
        if not self.trial_ends_at:
            return 0
        remaining = self.trial_ends_at - timezone.now()
        return max(0, remaining.days)
    
    def clean(self):
        """Validate GST registration consistency."""
        if self.is_gst_registered and not self.gst_reg_no:
            raise ValidationError({
                'gst_reg_no': 'GST registration number is required when GST registered.'
            })
        super().clean()


class OrganizationMembership(models.Model):
    """Organization membership with roles."""
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    # Permissions (cached for performance)
    permissions = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )
    
    # Timestamps
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invited_memberships'
    )
    
    class Meta:
        db_table = 'organization_memberships'
        unique_together = [('organization', 'user')]
        indexes = [
            models.Index(fields=['organization', 'user']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role})"