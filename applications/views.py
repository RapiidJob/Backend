# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Application, WorkHistory, WorkInProgress
from .serializers import (
        ApplicationCreateSerializer, ApplicationSerializer, 
        WorkHistorySerializer, WorkinProgressSerializer
    )
from RapidJob.permissions import IsWorker, IsEmployer
from RapidJob import pagination

class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsWorker]

    def perform_create(self, serializer):
        try:
            serializer.save(worker=self.request.user)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    pagination_class = pagination.StandardPageNumberPagination
    
    filter_backends = ['ordering']  
    ordering_fields = ['-created_at', 'category']  # Allow ordering by creation date (descending) and category


    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
class ApplicationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Application.DoesNotExist:
            return Response({"message": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        # application = self.get_object()
        # if application.
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Application.DoesNotExist:
            return Response({"message": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated]
    
    pagination_class = pagination.StandardPageNumberPagination
    
    filter_backends = ['ordering']  
    ordering_fields = ['-created_at', 'category']  # Allow ordering by creation date (descending) and category


    def perform_create(self, serializer):
        try:
            serializer.save(worker=self.request.user)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkHistoryRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated]
    

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except WorkHistory.DoesNotExist:
            return Response({"message": "Work history not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except WorkHistory.DoesNotExist:
            return Response({"message": "Work history not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ApplicationByUserAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsWorker]
    
    pagination_class = pagination.StandardPageNumberPagination
    
    filter_backends = ['ordering']  
    ordering_fields = ['-created_at', 'category']  # Allow ordering by creation date (descending) and category

    def get_queryset(self):
        return super().get_queryset().filter(worker=self.request.user)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ApplicationByJobAPView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsWorker]
    
    pagination_class = pagination.StandardPageNumberPagination
    
    filter_backends = ['ordering']  
    ordering_fields = ['-created_at', 'category']  # Allow ordering by creation date (descending) and category


    def get_queryset(self):
        return super().get_queryset().filter(job=self.request.query_params.get('job_id'))

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkInProgressCreateAPIView(generics.CreateAPIView):
    queryset = WorkInProgress.objects.all()
    serializer_class = WorkinProgressSerializer
    
    pagination_class = pagination.StandardPageNumberPagination
    
    filter_backends = ['ordering']  
    ordering_fields = ['-created_at', 'category']  # Allow ordering by creation date (descending) and category


    def perform_create(self, serializer):
        return super().perform_create(serializer)

class WorkInProgressRetrieveAPIView(generics.ListAPIView):
    queryset = WorkInProgress.objects.all()
    serializer_class = WorkinProgressSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class WorkInProgressUpdateAPIVIew(generics.UpdateAPIView):
    queryset = WorkInProgress.objects.all()
    lookup_field = 'pk'
    serializer_class= WorkinProgressSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class WorkInProgressDestoryAPiView(generics.DestroyAPIView):
    queryset =WorkInProgress.objects.all()
    lookup_field = 'pk'
    serializer_class = WorkinProgressSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
