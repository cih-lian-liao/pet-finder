"""
URL configuration for Pet Finder project.

The `urlpatterns` list routes URLs to views. This configuration defines
all the URL patterns for the pet finder application.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from website.views import (
    HomePageView, ClearPetsView, DownloadPetsView, 
    PetDetailView, PetStatsView
)

app_name = 'pet_finder'

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Main application URLs
    path('', HomePageView.as_view(), name='home'),
    path('clear/', ClearPetsView.as_view(), name='clear_pets'),
    path('download/', DownloadPetsView.as_view(), name='download_pets'),
    path('pet/<int:pet_id>/', PetDetailView.as_view(), name='pet_detail'),
    path('stats/', PetStatsView.as_view(), name='pet_stats'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
