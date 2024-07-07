# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('employer/create/', views.EmployerProfileCreateAPIView.as_view(), name='employer-create'),
    path('employer/<int:pk>/', views.EmployerProfileRetrieveUpdateAPIView.as_view(), name='employer-detail-update'),
    path('worker/create/', views.WorkerProfileCreateAPIView.as_view(), name='worker-create'),
    path('worker/<int:pk>/', views.WorkerProfileRetrieveUpdateAPIView.as_view(), name='worker-detail-update'),
]
