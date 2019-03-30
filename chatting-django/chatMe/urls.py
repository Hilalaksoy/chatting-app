from django.contrib.auth import views as auth_views
from rest_framework import routers
from django.urls import path
from .views import index

chatMe_router = routers.DefaultRouter()

# vcase_router.register('vcase-api/cases',VCaseViewSet)

chatMe_urlpatterns = [
    path('', index),
]
