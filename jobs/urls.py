from django.urls import path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
from .views import (
    JobCreateAPIView,JobRetrieveAPIView, 
    JobRetrieveUpdateAPIView, JobListAPIView,
    SearchDefaultView, SearchByPlaceView, 
    SearchbyLocationView, JobListByCategoryAPIView, JobListByUserAPIView, JobCatagoryAPIView
)

urlpatterns = [
    path('catagories/', JobCatagoryAPIView.as_view(), name="catagories"),
    path('list_by_user/', JobListByUserAPIView.as_view(), name="list_by_user"),
    path('category/', JobListByCategoryAPIView.as_view(), name="category"),
    path('list', JobListAPIView.as_view(), name='job-list'),
    path('create/', JobCreateAPIView.as_view(), name='job-create'),
    path('<int:pk>/', JobRetrieveUpdateAPIView.as_view(), name='job-detail'),
    path('get/<int:pk>/', JobRetrieveAPIView.as_view(), name="retrive"),
    path('search/', SearchDefaultView.as_view(), name='default-job-search'), # default search that searches based on the address of the worker's profile address
    path('search_by_location/', SearchbyLocationView.as_view()), # search based on lattitude and longitude of the worker's location
    path('search_by_place/', SearchByPlaceView.as_view(), name="search-by-place"), # Search based on place filled by the worker.
]
