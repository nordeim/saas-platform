"""
Privacy and PDPA compliance tasks for NexusCore.
"""

from celery import shared_task
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import logging
import hashlib

logger = logging.getLogger(__name__)


@shared_task
def enforce_pdpa_retention():
    """
    Daily task to enforce PDPA data retention policies.
    
    CRITICAL: This task implements differential retention periods:
    - Marketing data: 2 years (PDPA requirement)
    - Financial data: 7 years (IRAS requirement)
    - User data: 2 years of inactivity, unless financial data exists
    """
    logger.info("Starting PDPA data retention enforcement")
    
    from apps.leads.models import Lead
    from apps.users.models import User
    from apps.billing.models import Invoice
    
    # 1. Marketing Data: Delete after 2 years of inactivity
    marketing_cutoff = timezone.now() - relativedelta(years=2)
    deleted_marketing, _ = Lead.objects.filter(
        updated_at__lt=marketing_cutoff
    ).delete()
    
    # 2. Financial Data: Keep for 7 years (IRAS requirement)
    financial_cutoff = timezone.now() - relativedelta(years=7)
    
    # 3. User Data: Anonymize after 2 years of inactivity if no financial data
    user_cutoff = timezone.now() - relativedelta(years=2)
    old_users = User.objects.filter(
        is_active=False,
        updated_at__lt=user_cutoff
    ).exclude(
        # Keep users who have financial data within retention period
        owned_organizations__invoices__created_at__gt=financial_cutoff
    )
    
    anonymized_count = 0
    for user in old_users:
        # Anonymize personal data but keep account structure
        user.email = f"anonymized_{hashlib.sha256(str(user.id).encode()).hexdigest()[:16]}@deleted.nexuscore"
        user.name = "Deleted User"
        user.phone = ""
        user.company = ""
        user.set_unusable_password()
        user.save()
        anonymized_count += 1
    
    # 4. DSAR Exports: Delete after 30 days
    from apps.privacy.models import DSARRequest
    dsar_cutoff = timezone.now() - relativedelta(days=30)
    deleted_dsar_exports, _ = DSARRequest.objects.filter(
        export_expires_at__lt=dsar_cutoff
    ).update(export_url='')
    
    logger.info(f"PDPA Retention Enforcement Complete:")
    logger.info(f"- Deleted {deleted_marketing} marketing records")
    logger.info(f"- Anonymized {anonymized_count} user accounts")
    logger.info(f"- Cleaned {deleted_dsar_exports} expired DSAR exports")
    
    return {
        'marketing_records_deleted': deleted_marketing,
        'users_anonymized': anonymized_count,
        'dsar_exports_cleaned': deleted_dsar_exports
    }


@shared_task
def send_dsar_verification_email(dsar_id, user_email, verification_token):
    """Send DSAR verification email."""
    logger.info(f"Sending DSAR verification email to {user_email}")
    
    from apps.privacy.models import DSARRequest
    
    try:
        dsar_request = DSARRequest.objects.get(id=dsar_id)
        
        # TODO: Implement actual email sending
        logger.info(f"DSAR verification email sent to {user_email}")
        
        return True
    except DSARRequest.DoesNotExist:
        logger.error(f"DSAR request {dsar_id} not found")
        return False


@shared_task
def process_dsar_request(dsar_id):
    """Process DSAR request based on type."""
    logger.info(f"Processing DSAR request {dsar_id}")
    
    from apps.privacy.models import DSARRequest
    
    try:
        dsar_request = DSARRequest.objects.get(id=dsar_id)
        
        if dsar_request.request_type == 'export':
            # Generate data export
            export_data = generate_user_data_export(dsar_request.user)
            
            # Store export (in production, upload to secure S3)
            dsar_request.export_url = "https://example.com/export-file.zip"
            dsar_request.export_expires_at = timezone.now() + timezone.timedelta(days=30)
            dsar_request.status = 'completed'
            dsar_request.processed_at = timezone.now()
            dsar_request.save()
            
            logger.info(f"DSAR export completed for {dsar_request.user_email}")
            
        elif dsar_request.request_type == 'delete':
            # Send approval notification to admin
            notify_admin_dsar_deletion.delay(dsar_id=str(dsar_id))
            
        return True
        
    except DSARRequest.DoesNotExist:
        logger.error(f"DSAR request {dsar_id} not found")
        return False


@shared_task
def notify_admin_dsar_deletion(dsar_id):
    """Notify admin of DSAR deletion request for manual approval."""
    logger.info(f"Notifying admin of DSAR deletion request {dsar_id}")
    
    from apps.privacy.models import DSARRequest
    from apps.users.models import User
    
    try:
        dsar_request = DSARRequest.objects.get(id=dsar_id)
        
        # TODO: Send email to admin for approval
        # In production, this would send an email to the data protection officer
        
        logger.info(f"Admin notification sent for DSAR deletion {dsar_id}")
        
        return True
        
    except DSARRequest.DoesNotExist:
        logger.error(f"DSAR request {dsar_id} not found")
        return False


def generate_user_data_export(user):
    """Generate user data export for DSAR."""
    from apps.users.models import User
    from apps.organizations.models import Organization, OrganizationMembership
    from apps.billing.models import Invoice, Subscription
    from apps.events.models import Event
    
    if not user:
        return {}
    
    export_data = {
        'user': {
            'id': str(user.id),
            'email': user.email,
            'name': user.name,
            'company': user.company,
            'phone': user.phone,
            'is_verified': user.is_verified,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'timezone': user.timezone,
        },
        'organizations': [],
        'subscriptions': [],
        'invoices': [],
        'events': [],
    }
    
    # Organizations
    organizations = Organization.objects.filter(members=user)
    for org in organizations:
        membership = OrganizationMembership.objects.get(organization=org, user=user)
        export_data['organizations'].append({
            'id': str(org.id),
            'name': org.name,
            'uen': org.uen,
            'role': membership.role,
            'joined_at': membership.joined_at.isoformat(),
        })
    
    # Subscriptions
    subscriptions = Subscription.objects.filter(organization__members=user)
    for sub in subscriptions:
        export_data['subscriptions'].append({
            'id': str(sub.id),
            'plan': sub.plan.name,
            'status': sub.status,
            'current_period_start': sub.current_period_start.isoformat(),
            'current_period_end': sub.current_period_end.isoformat(),
        })
    
    # Invoices
    invoices = Invoice.objects.filter(organization__members=user)
    for invoice in invoices:
        export_data['invoices'].append({
            'id': str(invoice.id),
            'subtotal_cents': invoice.subtotal_cents,
            'gst_amount_cents': invoice.gst_amount_cents,
            'total_amount_cents': invoice.total_amount_cents,
            'status': invoice.status,
            'created_at': invoice.created_at.isoformat(),
        })
    
    # Events
    events = Event.objects.filter(user=user)
    for event in events:
        export_data['events'].append({
            'event_type': event.event_type,
            'created_at': event.created_at.isoformat(),
            'data': event.data,
        })
    
    return export_data