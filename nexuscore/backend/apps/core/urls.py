"""
Core URLs for NexusCore.
"""

from django.urls import path
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils import timezone


def health_check(request):
    """Health check endpoint for monitoring."""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '3.1.0'
    })


def ready_check(request):
    """Readiness check for Kubernetes."""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'ready',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'error': str(e)
        }, status=503)


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('ready/', ready_check, name='ready_check'),
]