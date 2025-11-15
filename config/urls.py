"""
URL Configuration for Prompt2Action AI Platform
Author: Cavin Otieno
Contact: cavin.otieno012@gmail.com
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # API routes (to be implemented)
    # path('api/', include('api.urls')),
    
    # Agent routes (to be implemented)
    # path('agents/', include('agents.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = "Prompt2Action AI Administration"
admin.site.site_title = "Prompt2Action AI Admin"
admin.site.index_title = "Welcome to Prompt2Action AI Platform"
