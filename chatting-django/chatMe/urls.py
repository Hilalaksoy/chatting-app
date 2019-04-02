from django.contrib.auth import views as auth_views
from rest_framework import routers
from django.urls import path
from .views import Login, MainPage, logout_view

chatMe_router = routers.DefaultRouter()

# vcase_router.register('vcase-api/cases',VCaseViewSet)

chatMe_urlpatterns = [
    path('', MainPage.as_view()),
    path('login/', Login.as_view()),
    path('logout/', logout_view),
]
