from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Job, JobAddress, JobCategory, JobSubcategory, UserSavedJob
from .serializers import JobSerializer, JobAddressSerializer, JobCatagoryReadSerializer, SavedJobSerializer
from django.db.models import Q
from RapidJob.permissions import IsEmployer, IsWorker
from rest_framework.exceptions import ValidationError
from .utils import haversine, create_job_address_from_user
from RapidJob import pagination
from rest_framework.decorators import action


class JobCreateAPIView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            
            if request.data.get("use_my_address") == 'False':
                city = request.data.get("city", None)
                country = request.data.get("country", None)
                region = request.data.get("region", None)
                latitude = request.data.get("latitude", None)
                longitude = request.data.get("longitude", None)
                job_address = JobAddress.objects.create(
                    city=city,
                    country=country, 
                    region=region,
                    latitude=latitude,
                    longitude=longitude,
                )
            else:
                if not request.user.address:
                    return Response({"message" : "You don't have address information"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    job_address = create_job_address_from_user(request.user)
            
            job = serializer.save(job_address=job_address)
            response = serializer.data
            response['job_address'] = JobAddressSerializer(instance=job.job_address).data
            return Response(response, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if request.user != instance.posted_by:
                return Response({"errors": "You do not have permission to update this job."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            job = serializer.save()
            
            if request.data.get("use_my_address") == 'False':
                city = request.data.get("city", None)
                country = request.data.get("country", None)
                region = request.data.get("region", None)
                latitude = request.data.get("latitude", None)
                longitude = request.data.get("longitude", None)
                
                address = job.job_address
                address.city = city
                address.country = country
                address.region = region
                address.latitude = latitude
                address.longitude = longitude
                address.save()
            else:
                job.job_address = request.user.address
            
            job.save()
            response = serializer.data
            response['job_address'] = JobAddressSerializer(instance=job.job_address).data
            return Response(response, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        except Job.DoesNotExist:
            return Response({"message": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    
class JobListByUserAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    pagination_class = pagination.StandardPageNumberPagination  # Enable pagination by default

    filter_backends = ['ordering']  # Allow ordering by fields
    ordering_fields = ['-created_at', 'category']  # Allow ordering by creation date (descending) and category

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(posted_by=user)
    
class JobListByCategoryAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]  
    pagination_class = pagination.StandardPageNumberPagination  

    filter_backends = ['ordering']  
    ordering_fields = ['-created_at', 'category']  # Allow ordering by creation date (descending) and category

    def get_queryset(self):
        queryset = self.queryset.filter(category=self.request.query_params.get('category'))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JobRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]



class SearchDefaultView(generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get('keyword', None)
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        largest_price = request.query_params.get('largest_price', 'false').lower() == 'true'
        smallest_price = request.query_params.get('smallest_price', 'false').lower() == 'true'
        newest = request.query_params.get('newest', 'false').lower() == 'true'
        oldest = request.query_params.get('oldest', 'false').lower() == 'true'

        jobs = Job.objects.all()

        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(subcategory__name__icontains=keyword) |
                Q(category__name__icontains=keyword)
            )

        if largest_price:
            jobs = jobs.order_by('-price')
        elif smallest_price:
            jobs = jobs.order_by('price')

        if newest:
            jobs = jobs.order_by('-created_at')
        elif oldest:
            jobs = jobs.order_by('created_at')
        
        def job_within_distance(job):
                if job.job_address and job.job_address.latitude and job.job_address.longitude:
                    return haversine(latitude, longitude, float(job.job_address.latitude), float(job.job_address.longitude)) <= 5000
                return False
        if latitude and longitude:
            jobs = list(filter(job_within_distance, jobs))
        paginator = pagination.StandardPageNumberPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
class SearchByPlaceView(generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.StandardPageNumberPagination

    def post(self, request, *args, **kwargs):
        category = request.data.get('category')
        title = request.data.get('title')
        country = request.data.get('country')
        region = request.data.get('region')
        city = request.data.get('city')

        try:
            if not country or not region or not city:
                return Response({"errors": "Country, region, and city are required for this search."}, status=status.HTTP_400_BAD_REQUEST)

            jobs = Job.objects.filter(
                Q(job_address__country__icontains=country) |
                Q(job_address__region__icontains=region) |
                (Q(job_address__city__icontains=city) & Q(job_address__city__isnull=True))
            )
            
            if title and category:
                jobs = jobs.filter(
                    Q(subcategory__name__icontains=category) |
                    Q(title__icontains=title)
                )
            elif title:
                jobs = jobs.filter(Q(title__icontains=title))
            elif category:
                jobs = jobs.filter(Q(subcategory__name__icontains=category))
            
            
            paginator = pagination.StandardPageNumberPagination()
            paginated_jobs = paginator.paginate_queryset(jobs, request)
            serializer = JobSerializer(paginated_jobs, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JobCatagoryAPIView(generics.ListAPIView):
    queryset = JobCategory.objects.all()
    serializer_class = JobCatagoryReadSerializer
    permission_classes = [AllowAny]

class SearchbyLocationView(generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.StandardPageNumberPagination

    def post(self, request, *args, **kwargs):
        category = request.data.get('category', None)
        title = request.data.get('title', None)
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        max_distance_km = 5000  # search within 5 km radius

        try:
            if not latitude or not longitude:
                return Response({"errors": "Latitude and longitude are required for this search."}, status=status.HTTP_400_BAD_REQUEST)

            jobs = Job.objects.all()

            if title and category:
                jobs = jobs.filter(
                    Q(subcategory__name__icontains=category) |
                    Q(title__icontains=title)
                )
            elif title:
                jobs = jobs.filter(Q(title__icontains=title))
            elif category:
                jobs = jobs.filter(Q(subcategory__name__icontains=category))

            def job_within_distance(job):
                if job.job_address and job.job_address.latitude and job.job_address.longitude:
                    return haversine(latitude, longitude, float(job.job_address.latitude), float(job.job_address.longitude)) <= max_distance_km
                return False
            
            jobs = list(filter(job_within_distance, jobs))

            paginator = pagination.StandardPageNumberPagination()
            paginated_jobs = paginator.paginate_queryset(jobs, request)
            serializer = JobSerializer(paginated_jobs, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        except ValueError:
            return Response({"errors": "Invalid latitude or longitude values."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchByKeyWordAPIView(generics.GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.StandardPageNumberPagination

    def post(self, request, *args, **kwargs):
        keyword = request.data.get('key_word', None)

        try:
            if not keyword:
                return Response({'errors': 'Key word needed for this search'}, status=status.HTTP_400_BAD_REQUEST)
            jobs = Job.objects.all()
            jobs = jobs.filter(
                Q(subcategory__name__icontains=keyword) |
                Q(title__icontains=keyword) | 
                Q(job_address__country__icontains=keyword) |
                Q(job_address__region__icontains=keyword) |
                (Q(job_address__city__icontains=keyword) & Q(job_address__city__isnull=True)) | 
                Q(description__icontains=keyword)
            ) 

            paginator = pagination.StandardPageNumberPagination()
            paginated_jobs = paginator.paginate_queryset(jobs, request)
            serializer = JobSerializer(paginated_jobs, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserSavedJobListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserSavedJob.objects.all()
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.StandardPageNumberPagination
    
    # filter_backends = ['ordering']  
    # ordering_fields = ['-created_at', 'title']  # Allow ordering by creation date (descending) and category


    def get_queryset(self):
        # Filter queryset to only include saved jobs of the current user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user based on the request's authenticated user
        serializer.save(user=self.request.user)

class UserSavedJobRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSavedJob.objects.all()
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter queryset to only include saved jobs of the current user
        return self.queryset.filter(user=self.request.user)