"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from core.views import home, about
except ImportError:
    from views import home, about

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Public pages
    path('', home, name='home'),
    path('about/', about, name='about'),
    
    # Accounts
    path('accounts/', include('accounts.urls')),
    
    # Detection
    path('detection/', include('detection.urls')),
    
    # Contact
    path('contact/', include('contact.urls')),
    
    # Admin Panel
    path('admin-panel/', include('admin_panel.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
