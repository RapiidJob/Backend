# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Application, WorkHistory
from .serializers import ApplicationCreateSerializer, ApplicationSerializer, WorkHistorySerializer
from RapidJob.permissions import IsWorker, IsEmployer

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
