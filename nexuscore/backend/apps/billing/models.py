"""
Billing models for NexusCore with Singapore GST compliance.
"""

import uuid
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from apps.organizations.models import Organization
from apps.users.models import User


class Plan(models.Model):
    """Subscription plan definitions."""
    
    BILLING_PERIOD_CHOICES = [
        ('month', 'Monthly'),
        ('year', 'Annual'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Pricing
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    billing_period = models.CharField(max_length=10, choices=BILLING_PERIOD_CHOICES, default='month')
    amount_cents = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default='SGD')
    
    # Features
    features = models.JSONField(default=dict, blank=True)
    limits = models.JSONField(default=dict, blank=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    # Stripe integration
    stripe_price_id = models.CharField(max_length=255, blank=True, db_index=True)
    stripe_product_id = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plans'
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['is_active', 'is_visible']),
            models.Index(fields=['stripe_price_id']),
        ]
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.name} ({self.billing_period})"
    
    @property
    def amount_dollars(self):
        """Return amount in dollars (SGD)."""
        return self.amount_cents / 100
    
    @property
    def annual_amount_cents(self):
        """Calculate annual amount if monthly."""
        if self.billing_period == 'year':
            return self.amount_cents
        return self.amount_cents * 12
    
    @property
    def savings_percentage(self):
        """Calculate savings for annual billing."""
        if self.billing_period == 'year':
            monthly_equivalent = self.amount_cents / 12
            try:
                monthly_plan = Plan.objects.get(
                    sku=f"{self.sku.split('-')[0]}-month",
                    is_active=True
                )
                if monthly_plan:
                    return int(((monthly_plan.amount_cents - monthly_equivalent) / monthly_plan.amount_cents) * 100)
            except Plan.DoesNotExist:
                pass
        return 0


class Subscription(models.Model):
    """Customer subscription state."""
    
    STATUS_CHOICES = [
        ('trialing', 'Trialing'),
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('unpaid', 'Unpaid'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trialing')
    cancel_at_period_end = models.BooleanField(default=False)
    
    # Billing period
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    
    # Trial information
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    
    # Stripe integration
    stripe_subscription_id = models.CharField(max_length=255, unique=True, db_index=True)
    stripe_customer_id = models.CharField(max_length=255, db_index=True)
    stripe_latest_invoice_id = models.CharField(max_length=255, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'subscriptions'
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['status', 'current_period_end']),
            models.Index(fields=['stripe_subscription_id']),
            models.Index(fields=['created_at']),
            # Partial index for active subscriptions
            models.Index(
                fields=['organization'],
                condition=models.Q(status__in=['active', 'trialing']),
                name='idx_active_subscriptions'
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(current_period_end__gt=models.F('current_period_start')),
                name='period_end_after_start'
            ),
            models.CheckConstraint(
                check=~models.Q(status='trialing') | models.Q(trial_end__isnull=False),
                name='trial_status_requires_trial_end'
            ),
        ]
    
    def __str__(self):
        return f"{self.organization.name} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self):
        """Check if subscription is active or trialing."""
        return self.status in ['active', 'trialing']
    
    @property
    def days_until_renewal(self):
        """Days until subscription renews."""
        remaining = self.current_period_end - timezone.now()
        return max(0, remaining.days)
    
    @property
    def is_in_trial(self):
        """Check if subscription is in trial period."""
        if not self.trial_end:
            return False
        return timezone.now() < self.trial_end and self.status == 'trialing'
    
    def clean(self):
        """Django 6.0 model validation."""
        if self.trial_end and self.trial_end <= timezone.now():
            raise ValidationError({
                'trial_end': 'Trial end must be in the future.'
            })
        
        if self.current_period_end <= self.current_period_start:
            raise ValidationError({
                'current_period_end': 'Period end must be after period start.'
            })
        
        super().clean()


class Invoice(models.Model):
    """GST-compliant invoice with Django 6.0 GeneratedField."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('uncollectible', 'Uncollectible'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,
        blank=True
    )
    
    # Monetary Values (in cents) [CRITICAL]
    subtotal_cents = models.BigIntegerField(help_text="Net amount before tax in cents")
    gst_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0900)
    
    # DJANGO 6.0 FEATURE: Database-computed GST Amount [CRITICAL]
    gst_amount_cents = models.GeneratedField(
        expression=models.Func(
            models.F('subtotal_cents') * models.F('gst_rate'),
            function='ROUND',
            output_field=models.BigIntegerField()
        ),
        output_field=models.BigIntegerField(),
        db_persist=True
    )
    
    # DJANGO 6.0 FEATURE: Database-computed Total [CRITICAL]
    total_amount_cents = models.GeneratedField(
        expression=models.F('subtotal_cents') + models.F('gst_amount_cents'),
        output_field=models.BigIntegerField(),
        db_persist=True
    )
    
    # IRAS Compliance [CRITICAL]
    iras_transaction_code = models.CharField(
        max_length=10,
        choices=[
            ('SR', 'Standard Rate'),
            ('ZR', 'Zero Rate'),
            ('OS', 'Out of Scope'),
            ('TX', 'Taxable Supply')
        ],
        default='SR'
    )
    
    # Payment tracking
    amount_paid_cents = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=3, default='SGD')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    paid = models.BooleanField(default=False)
    
    # Dates
    due_date = models.DateTimeField()
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # External References
    pdf_url = models.URLField(blank=True)
    stripe_invoice_id = models.CharField(max_length=255, unique=True, db_index=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    
    # Data
    line_items = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'invoices'
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['status', 'due_date']),
            models.Index(fields=['stripe_invoice_id']),
            models.Index(fields=['created_at']),
            # Partial index for overdue invoices
            models.Index(
                fields=['due_date'],
                condition=models.Q(status='open') & models.Q(due_date__lt=timezone.now()),
                name='idx_overdue_invoices'
            ),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount_paid_cents__lte=models.F('total_amount_cents')),
                name='amount_paid_not_exceed_due'
            ),
            models.CheckConstraint(
                check=~models.Q(paid=True) | models.Q(paid_at__isnull=False),
                name='paid_invoices_require_paid_at'
            ),
            models.CheckConstraint(
                check=models.Q(subtotal_cents__gte=0),
                name='positive_subtotal'
            )
        ]
    
    def __str__(self):
        return f"Invoice {self.id} - {self.organization.name}"
    
    @property
    def subtotal_dollars(self):
        """Amount due in dollars."""
        return self.subtotal_cents / 100
    
    @property
    def gst_amount_dollars(self):
        """GST amount in dollars."""
        return self.gst_amount_cents / 100
    
    @property
    def total_amount_dollars(self):
        """Total amount in dollars."""
        return self.total_amount_cents / 100
    
    @property
    def is_overdue(self):
        """Check if invoice is overdue."""
        return self.status == 'open' and timezone.now() > self.due_date
    
    @property
    def days_overdue(self):
        """Days overdue if invoice is overdue."""
        if not self.is_overdue:
            return 0
        overdue = timezone.now() - self.due_date
        return overdue.days
    
    def clean(self):
        """Validate invoice data."""
        if self.paid and not self.paid_at:
            raise ValidationError({
                'paid_at': 'Paid invoices must have a paid_at timestamp.'
            })
        super().clean()


class IdempotencyRecord(models.Model):
    """Idempotency records for preventing duplicate operations (from PRD-d-3)."""
    
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255, unique=True, db_index=True)
    request_path = models.CharField(max_length=255)
    request_method = models.CharField(max_length=10)
    request_hash = models.CharField(max_length=64)  # SHA256 of request body
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response_status_code = models.IntegerField(null=True, blank=True)
    response_body = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'idempotency_records'
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['request_path', 'request_method']),
        ]
    
    def __str__(self):
        return f"Idempotency: {self.key}"
    
    def is_expired(self):
        """Check if idempotency record has expired."""
        return timezone.now() > self.expires_at