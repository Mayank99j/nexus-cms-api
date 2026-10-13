"""
URL configuration for Nexus Headless CMS.
"""
from django.contrib import admin
from django.urls import path, include
from cms.views import home_view, article_detail_view

urlpatterns = [
    # Editorial Admin Portal
    path('admin/', admin.site.urls),

    # REST API endpoints
    path('api/', include('cms.urls')),

    # Consumer-facing publication frontend
    path('', home_view, name='home'),
    path('article/<slug:slug>/', article_detail_view, name='article_detail'),
]
