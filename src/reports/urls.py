from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
