from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import user_login_view, user_register_view


router = DefaultRouter()

urlpatterns = [
    path(r'users/login/', user_login_view),
    path(r'users/register/', user_register_view),
]
