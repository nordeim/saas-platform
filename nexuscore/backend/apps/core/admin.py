"""
Django admin configuration for NexusCore.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.users.models import User
from apps.organizations.models import Organization, OrganizationMembership
from apps.billing.models import Plan, Invoice, Subscription
from apps.privacy.models import DSARRequest
from apps.leads.models import Lead


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with Django 6.0 features."""
    
    list_display = ['email', 'name', 'is_verified', 'is_active', 'created_at']
    list_filter = ['is_verified', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'name', 'company']
    ordering = ['-created_at']
    
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Personal Info', {'fields': ['name', 'company', 'phone']}),
        ('Permissions', {'fields': ['is_verified', 'is_active', 'is_staff', 'is_superuser']}),
        ('Important Dates', {'fields': ['last_login', 'created_at']}),
        ('Preferences', {'fields': ['timezone', 'email_preferences']}),
    ]
    
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'name', 'password1', 'password2'],
        }),
    ]
    
    readonly_fields = ['created_at', 'last_login']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Organization admin with Singapore compliance."""
    
    list_display = ['name', 'uen', 'is_gst_registered', 'owner', 'created_at']
    list_filter = ['is_gst_registered', 'created_at']
    search_fields = ['name', 'uen', 'billing_email']
    ordering = ['-created_at']
    
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'owner']}),
        ('Singapore Compliance', {
            'fields': ['uen', 'is_gst_registered', 'gst_reg_no'],
            'classes': ['collapse']
        }),
        ('Billing', {
            'fields': ['stripe_customer_id', 'billing_email', 'billing_phone', 'billing_address'],
            'classes': ['collapse']
        }),
        ('Settings', {'fields': ['timezone', 'locale', 'settings', 'trial_ends_at']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    """Organization membership admin."""
    
    list_display = ['organization', 'user', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['organization__name', 'user__email']
    ordering = ['-joined_at']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Plan admin with pricing display."""
    
    list_display = ['name', 'sku', 'billing_period', 'amount_dollars', 'is_active', 'display_order']
    list_filter = ['billing_period', 'is_active', 'is_visible']
    search_fields = ['name', 'sku', 'description']
    ordering = ['display_order', 'name']
    
    def amount_dollars(self, obj):
        return f"${obj.amount_cents / 100:.2f}"
    amount_dollars.short_description = 'Amount (SGD)'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Invoice admin with GST compliance display."""
    
    list_display = ['id', 'organization', 'total_amount_dollars', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'iras_transaction_code', 'created_at']
    search_fields = ['organization__name', 'stripe_invoice_id']
    ordering = ['-created_at']
    
    fieldsets = [
        (None, {'fields': ['organization', 'subscription', 'status']}),
        ('GST Compliance', {
            'fields': ['subtotal_cents', 'gst_rate', 'gst_amount_cents', 'total_amount_cents', 'iras_transaction_code'],
            'classes': ['collapse']
        }),
        ('Payment', {
            'fields': ['amount_paid_cents', 'paid', 'paid_at'],
            'classes': ['collapse']
        }),
        ('External', {'fields': ['stripe_invoice_id', 'stripe_payment_intent_id', 'pdf_url']}),
        ('Data', {'fields': ['due_date', 'line_items', 'metadata']}),
    ]
    
    readonly_fields = ['gst_amount_cents', 'total_amount_cents', 'created_at']
    
    def total_amount_dollars(self, obj):
        return f"${obj.total_amount_cents / 100:.2f}"
    total_amount_dollars.short_description = 'Total (SGD)'


@admin.register(DSARRequest)
class DSARRequestAdmin(admin.ModelAdmin):
    """DSAR request admin for PDPA compliance."""
    
    list_display = ['id', 'user_email', 'request_type', 'status', 'sla_status', 'requested_at']
    list_filter = ['request_type', 'status', 'requested_at']
    search_fields = ['user_email', 'user__email']
    ordering = ['-requested_at']
    
    fieldsets = [
        (None, {'fields': ['user_email', 'user', 'request_type', 'status']}),
        ('Verification', {'fields': ['verified_at', 'verification_method']}),
        ('Processing', {'fields': ['export_url', 'export_expires_at', 'failure_reason']}),
        ('Deletion Approval', {'fields': ['deletion_approved_by', 'deletion_approved_at']}),
        ('Timestamps', {'fields': ['requested_at', 'processed_at']}),
    ]
    
    readonly_fields = ['requested_at', 'verification_token']
    
    def sla_status(self, obj):
        return obj.sla_status()
    sla_status.short_description = 'SLA Status'


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Lead admin for marketing tracking."""
    
    list_display = ['name', 'email', 'company', 'status', 'source', 'created_at']
    list_filter = ['status', 'source', 'created_at']
    search_fields = ['name', 'email', 'company']
    ordering = ['-created_at']
    
    fieldsets = [
        (None, {'fields': ['name', 'email', 'phone', 'company', 'job_title']}),
        ('Lead Details', {'fields': ['source', 'status', 'notes']}),
        ('UTM Tracking', {
            'fields': ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'],
            'classes': ['collapse']
        }),
        ('Form Data', {'fields': ['form_data']}),
        ('Timestamps', {'fields': ['created_at', 'converted_at']}),
    ]
    
    readonly_fields = ['created_at']


# Unregister the default Group model
admin.site.unregister(Group)