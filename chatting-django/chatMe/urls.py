from django.contrib.auth import views as auth_views
from rest_framework import routers
from django.urls import path
from .views import Login, MainPage, logout_view,Register
from .apis import ChatViewSet

chatMe_router = routers.DefaultRouter()

chatMe_router.register('api/chat', ChatViewSet)

chatMe_urlpatterns = [
    path('', MainPage.as_view()),
    path('login/', Login.as_view()),
    path('logout/', logout_view),
    path('register/', Register.as_view()),
]
