from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('admin_honeypot.urls'), name='fake-admin'),  # Route for fake admin URL to trap potential attackers
    path('elite/admin/', admin.site.urls),  # Actual admin URL
    path('api/user/', include('user.urls')),  # Include user-related API endpoints
    path('api/bill/', include('BillManagement.urls')),  # Include BillManagement API endpoints
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
