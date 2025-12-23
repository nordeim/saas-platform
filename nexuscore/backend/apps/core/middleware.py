"""
Core middleware for NexusCore with Django 6.0 features.
"""

from django.http import JsonResponse
from django.conf import settings
import time
import hashlib


class SecurityHeadersMiddleware:
    """Django 6.0 enhanced security headers middleware."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = (
            'accelerometer=(), camera=(), geolocation=(), '
            'gyroscope=(), magnetometer=(), microphone=(), '
            'payment=(), usb=()'
        )
        
        # HSTS Preload (only in production)
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = (
                'max-age=31536000; includeSubDomains; preload'
            )
        
        # Remove server header for security
        response['Server'] = ''
        
        return response


class RateLimitMiddleware:
    """Simple rate limiting middleware for authentication endpoints."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Only apply to authentication endpoints
        if request.path in ['/api/v1/auth/login/', '/api/v1/auth/register/']:
            from django.core.cache import cache
            
            cache_key = f"ratelimit:{request.META.get('REMOTE_ADDR')}:{request.path}"
            
            # Check rate limit
            request_count = cache.get(cache_key, 0)
            if request_count >= 5:  # 5 requests per minute
                return JsonResponse(
                    {'error': 'Too many requests. Please try again later.'},
                    status=429
                )
            
            # Increment counter
            cache.set(cache_key, request_count + 1, timeout=60)
        
        return self.get_response(request)


class CustomCSPMiddleware:
    """Custom CSP middleware for Singapore compliance."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add custom CSP headers for Singapore compliance
        csp_header = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://js.stripe.com https://www.googletagmanager.com; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https: https://*.stripe.com https://*.cloudfront.net; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.stripe.com https://www.google-analytics.com; "
            "frame-src 'self' https://js.stripe.com https://hooks.stripe.com; "
            "frame-ancestors 'none';"
        )
        
        response['Content-Security-Policy'] = csp_header
        
        return response