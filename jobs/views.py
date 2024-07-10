from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Job, JobAddress
from .serializers import JobSerializer, JobAddressSerializer
from django.db.models import Q
from RapidJob.permissions import IsEmployer, IsWorker

import math

class JobCreateAPIView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def create(self, request, *args, **kwargs):
        # if request.user.account_type != "Employer":
        #     return Response({"error": "Only employers can create jobs."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        if request.data.get("use_my_address") == 'False':
            city = request.data.get("city", None)
            country = request.data.get("country", None)
            region = request.data.get("region", None)
            latitude = request.data.get("latitude", None)
            longitude = request.data.get("longitude", None)
            address  = JobAddress.objects.create(
                city=city,
                country=country, 
                region=region,
                latitude=latitude,
                longitude=longitude,
                
            )
            job.job_adress = address
            job.save()
        else:
            job.job_adress = request.user.address
            job.save()
        response = serializer.data
        response['job_adress'] = JobAddressSerializer(instance=job.job_adress).data
        return Response(response, status=status.HTTP_201_CREATED)
    
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
        
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        job = serializer.save()
        
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
            Q(job_adress__country__icontains=address.country) |
            Q(job_adress__region__icontains=address.region) |
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

class SearchByPlaceView(generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsWorker]


    def post(self, request, *args, **kwargs):
        category = request.data.get('category')
        title = request.data.get('title')
        country = request.data.get('country')
        region = request.data.get('region')
        city = request.data.get('city')

        jobs = Job.objects.filter(
            Q(job_adress__country__icontains=country) |
            Q(job_adress__region__icontains=region) |
            (Q(job_adress__city__icontains=city) | Q(job_adress__city__isnull=True))
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

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    print(lat1, lat2)
    lat1 = float(lat1)
    lat2 = float(lat2)

    lon1 = float(lon1)
    lon2 = float(lon2)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c 


class SearchbyLocationView(generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsWorker]

    def post(self, request, *args, **kwargs):
        category = request.data.get('category', None)
        title = request.data.get('title', None)
        latitude = request.data.get('latitude')
        longitude = request.data.get('latitude')
        max_distance_km = 5000 # search by 5 km radius

        jobs = Job.objects.all()
        print(category, title)
        if title and category:
            jobs = jobs.filter(
                Q(subcategory__name__icontains=category) |
                Q(title__icontains=title)
            )
            
        elif title:
            jobs = jobs.filter(Q(title__icontains=title))
        elif category:
            jobs=jobs.filter(Q(subcategory__name__icontains=category))
        
        print(jobs)

        def job_within_distance(job):
            if job.job_address and job.job_address.latitude and job.job_address.longitude:
                print('hi', job)
                return haversine(latitude, longitude, float(job.job_address.latitude), float(job.job_address.longitude)) <= max_distance_km
            return False
        
        jobs = list(filter(job_within_distance, jobs))
        print(jobs)

        serializer  = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        

        
        








        





