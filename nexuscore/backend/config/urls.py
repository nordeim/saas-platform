"""
NexusCore URL configuration.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/v1/', include('apps.core.urls')),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.organizations.urls')),
    path('api/v1/', include('apps.subscriptions.urls')),
    path('api/v1/', include('apps.billing.urls')),
    path('api/v1/', include('apps.leads.urls')),
    path('api/v1/', include('apps.privacy.urls')),
    path('api/v1/', include('apps.webhooks.urls')),
    path('api/v1/', include('apps.events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns