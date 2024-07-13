# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('employer/create/', views.EmployerProfileCreateAPIView.as_view(), name='employer-create'),
    path('employer', views.EmployerProfileRetrieveUpdateAPIView.as_view(), name='employer-detail-update'),
    path('worker/create/', views.WorkerProfileCreateAPIView.as_view(), name='worker-create'),
    path('worker', views.WorkerProfileRetrieveUpdateAPIView.as_view(), name='worker-detail-update'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('employer/verify/<int:pk>/', views.EmployerProfileVerifyAPIView.as_view(), name='employer-profile-verify'),
    path('worker/verify/<int:pk>/', views.WorkerProfileVerifyAPIView.as_view(), name="worker-profile-verify"),
]
