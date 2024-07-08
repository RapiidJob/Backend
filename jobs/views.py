from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from RapidJob.permissions import IsEmployer, IsWorker

class JobCreateAPIView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def create(self, request, *args, **kwargs):
        # if request.user.account_type != "Employer":
        #     return Response({"error": "Only employers can create jobs."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class JobRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.account_type == "Employer":
            return Job.objects.none()  # Return an empty queryset if not an employer
        return Job.objects.filter(posted_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if request.user != instance.posted_by:
            return Response({"error": "You do not have permission to update this job."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

class JobRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
