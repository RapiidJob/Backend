from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessagesViewSet

router = DefaultRouter()
router.register(r'messages', MessagesViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
