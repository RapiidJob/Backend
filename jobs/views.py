from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from django.db.models import Q
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


class SearchDefaultView(generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsWorker]

    def post(self, request, *args, **kwargs):
        title = request.data.get('title', None)
        category = request.data.get('category', None)
        
        user_instance = request.user
        address = user_instance.address

        if not address:
            return Response({"error":"User addres is required for this search."}, status=status.HTTP_400_BAD_REQUEST)
        jobs = Job.objects.filter(
            Q(job_adress__country__icontains=address.country) &
            Q(job_adress__region__icontains=address.region) &
            (Q(job_adress__city__icontains=address.city) | Q(job_adress__city__isnull=True))
            )


        if title and category:
            jobs = jobs.filter(
                Q(subcategory__name__icontains=category) |
                Q(title__icontains=title)
            )
        elif title:
            jobs = jobs.filter(Q(title__icontains=title))
        elif category:
            jobs=jobs.filter(Q(subcategory__name__icontains=category))

        serializer  = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

