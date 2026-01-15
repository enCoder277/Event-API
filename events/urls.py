from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RegisterAPIView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('', include(router.urls)),
]
