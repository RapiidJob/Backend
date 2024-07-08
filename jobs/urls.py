from django.urls import path
from .views import JobCreateAPIView,JobRetrieveAPIView, JobRetrieveUpdateAPIView, JobListAPIView

urlpatterns = [
    path('', JobListAPIView.as_view(), name='job-list'),
    path('create/', JobCreateAPIView.as_view(), name='job-create'),
    path('<int:pk>/', JobRetrieveUpdateAPIView.as_view(), name='job-detail'),
    path('get/<int:pk>/', JobRetrieveAPIView.as_view(), name="retrive")
]
