from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import user_login_view, user_register_view

router = DefaultRouter()

router.routes += [
    path('login/', user_login_view),
    path('register/', user_register_view),
]

urlpatterns = [
    path('', include(router.urls)),
]
