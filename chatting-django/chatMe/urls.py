from django.contrib.auth import views as auth_views
from rest_framework import routers
from django.urls import path
from .views import login

chatMe_router = routers.DefaultRouter()

# vcase_router.register('vcase-api/cases',VCaseViewSet)

chatMe_urlpatterns = [
    path('', login),
    #path('login/',  login.as_view()),
]
