# urls.py (inside your Django app)

from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ApplicationListAPIView.as_view(), name='application-list'),
    path('create/', views.ApplicationCreateAPIView.as_view(), name='application-create'),
    path('<int:pk>/', views.ApplicationRetrieveUpdateAPIView.as_view(), name='application-detail'),
    path('workhistories/', views.WorkHistoryListCreateAPIView.as_view(), name='workhistory-list'),
    path('workhistories/<int:pk>/', views.WorkHistoryRetrieveUpdateAPIView.as_view(), name='workhistory-detail'),
    path('job_applications/', views.ApplicationByJobAPView.as_view(), name="retrive"),
    path("user_applications/", views.ApplicationByUserAPIView.as_view(), name="user_applications"),
]
