# views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Application, WorkHistory
from .serializers import ApplicationCreateSerializer, ApplicationSerializer, WorkHistorySerializer
from RapidJob.permissions import IsWorker, IsEmployer


class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsWorker]

    def perform_create(self, serializer):
        serializer.save(worker=self.request.user)

class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

class ApplicationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

class WorkHistoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(worker=self.request.user)

class WorkHistoryRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated]
