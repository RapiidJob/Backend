from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser, EmployerProfile, WorkerProfile
from .serializers import ( CustomUserRegisterSerializer, EmployerProfileSerializer,
                            WorkerProfileSerializer, LoginSerializer, 
                            CustomUserSerializer, UserAddressSerializer)

def password_reset_confirm_view(request, uid, token):
    return render(request, 'password_reset_confirm.html', {'uid': uid, 'token': token})

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate token
        refresh = RefreshToken.for_user(user)
        token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        response_data = serializer.data
        response_data['token'] = token_data
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        user_data = CustomUserSerializer(instance=user)
        
        response_data = {
            'user': user_data.data,
            'token': token_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class EmployerProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        user_instance = request.user
        user_data = {
            "email": user_instance.email,
            "first_name": request.data.get('first_name', user_instance.first_name),
            "last_name": request.data.get('last_name', user_instance.last_name),
            "birth_date": request.data.get('birth_date', user_instance.birth_date),
            "gender": request.data.get('gender', user_instance.gender),
            "phone_number": request.data.get('phone_number', user_instance.phone_number),
            "verification_type": request.data.get('verification_type', user_instance.verification_type),
            "verification_document": request.FILES.get('verification_document', user_instance.verification_document),
            "profile_image": request.FILES.get('profile_image', user_instance.profile_image),
            "account_type": user_instance.account_type,
            "is_identity_verified": user_instance.is_identity_verified,
            "is_email_verified": user_instance.is_email_verified,
            "is_phone_verified": user_instance.is_phone_verified,
            "rating": user_instance.rating,
            "created_at": user_instance.created_at,
        }
        
        if user_data['account_type'] != 'Employer':
            raise ValueError("User is not an employer")
 
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user_serializer = CustomUserSerializer(instance=user_instance, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            print("User serializer errors:", user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        address_data = {
            "country": request.data.get('address.country'),
            "region": request.data.get('address.region'),
            "city": request.data.get('address.city'),
            "kebele": request.data.get('address.kebele'),
            "house_number": request.data.get('address.house_number'),
            "latitude": request.data.get('address.latitude'),
            "longitude": request.data.get('address.longitude'),
            "is_permanent": request.data.get('address.is_permanent'),
        }
        print("reached here?")
        address_serializer = UserAddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address_instance = address_serializer.save()

        # Link address to user instance
        user_instance.address = address_instance
        user_instance.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class EmployerProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            profile = self.queryset.get(user=self.request.user)
            return profile
        except EmployerProfile.DoesNotExist:
            return Response({"error": "Employer profile not found."}, status=status.HTTP_404_NOT_FOUND)


class WorkerProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = WorkerProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        user_instance = request.user

        user_data = {
            "email": user_instance.email,
            "first_name": request.data.get('first_name', user_instance.first_name),
            "last_name": request.data.get('last_name', user_instance.last_name),
            "birth_date": request.data.get('birth_date', user_instance.birth_date),
            "gender": request.data.get('gender', user_instance.gender),
            "phone_number": request.data.get('phone_number', user_instance.phone_number),
            "verification_type": request.data.get('verification_type', user_instance.verification_type),
            "verification_document": request.FILES.get('verification_document', user_instance.verification_document),
            "profile_image": request.FILES.get('profile_image', user_instance.profile_image),
            "account_type": user_instance.account_type,
            "is_identity_verified": user_instance.is_identity_verified,
            "is_email_verified": user_instance.is_email_verified,
            "is_phone_verified": user_instance.is_phone_verified,
            "rating": user_instance.rating,
            "created_at": user_instance.created_at,
        }
        if user_data['account_type'] != 'Worker':
            raise ValueError("User is not an worker")
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user_serializer = CustomUserSerializer(instance=user_instance, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            print("User serializer errors:", user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address_data = {
            "country": request.data.get('address.country'),
            "region": request.data.get('address.region'),
            "city": request.data.get('address.city'),
            "kebele": request.data.get('address.kebele'),
            "house_number": request.data.get('address.house_number'),
            "latitude": request.data.get('address.latitude'),
            "longitude": request.data.get('address.longitude'),
            "is_permanent": request.data.get('address.is_permanent'),
        }

        address_serializer = UserAddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address_instance = address_serializer.save()

        # Link address to user instance
        user_instance.address = address_instance
        user_instance.save()
       
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WorkerProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = WorkerProfile.objects.all()
    serializer_class = WorkerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            profile = self.queryset.get(user=self.request.user)
            return profile
        except WorkerProfile.DoesNotExist:
            return Response({"error": "Worker profile not found."}, status=status.HTTP_404_NOT_FOUND)
