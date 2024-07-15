# views.py
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from RapidJob.permissions import IsAdmin
from .models import CustomUser, EmployerProfile, WorkerProfile
from .serializers import (CustomUserRegisterSerializer, EmployerProfileSerializer,
                          WorkerProfileSerializer, LoginSerializer, 
                          CustomUserSerializer, UserAddressSerializer)

def password_reset_confirm_view(request, uid, token):
    return render(request, 'password_reset_confirm.html', {'uid': uid, 'token': token})

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
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
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            user_data = CustomUserSerializer(instance=user)
            user_data = user_data.data
            worker_profile = None
            user_data['has_specialised_profile'] = True
            if user_data['account_type'] == "Worker":
                try:
                    worker_profile = WorkerProfile.objects.get(user=user)
                    user_data['plan'] = worker_profile.plan
                    user_data['last_paid'] = worker_profile.last_paid
                    # user_data['profile_image'] = worker_profile.profile_image
                except:
                    worker_profile = None
                    user_data['has_specialised_profile'] = False
            if user_data['account_type'] == "Employer":
                try:
                    employer_profile = EmployerProfile.objects.get(user=user)
                    user_data['plan'] = employer_profile.plan
                    user_data['last_paid'] = employer_profile.last_paid
                    # user_data['profile_image'] = employer_profile.profile_image
                except:
                    employer_profile = None
                    user_data['has_specialised_profile'] = False
                    
            response_data = {
                'user': user_data,
                'token': token_data\
            }
            
            
            return Response(response_data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class EmployerProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        try:
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
                return Response({"message": "User is not an employer"}, status=status.HTTP_400_BAD_REQUEST)
    
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            user_serializer = CustomUserSerializer(instance=user_instance, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            address_data = {
                "country": request.data.get('country'),
                "region": request.data.get('region'),
                "city": request.data.get('city'),
                "kebele": request.data.get('kebele'),
                "house_number": request.data.get('house_number'),
                "latitude": request.data.get('latitude'),
                "longitude": request.data.get('longitude'),
                "is_permanent": request.data.get('is_permanent'),
            }
            address_serializer = UserAddressSerializer(data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address_instance = address_serializer.save()

            # Link address to user instance
            user_instance.address = address_instance
            user_instance.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmployerProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            profile = self.queryset.get(user=self.request.user)
            return profile
        except EmployerProfile.DoesNotExist:
            return Response({"message": "Employer profile not found."}, status=status.HTTP_404_NOT_FOUND)

class WorkerProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = WorkerProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        try:
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
                return Response({"message": "User is not a worker"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user_serializer = CustomUserSerializer(instance=user_instance, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            address_data = {
                "country": request.data.get('country'),
                "region": request.data.get('region'),
                "city": request.data.get('city'),
                "kebele": request.data.get('kebele'),
                "house_number": request.data.get('house_number'),
                "latitude": request.data.get('latitude'),
                "longitude": request.data.get('longitude'),
                "is_permanent": request.data.get('is_permanent'),
            }
            address_serializer = UserAddressSerializer(data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address_instance = address_serializer.save()

            # Link address to user instance
            user_instance.address = address_instance
            user_instance.save()
           
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"message": "Validation error", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkerProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = WorkerProfile.objects.all()
    serializer_class = WorkerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            profile = self.queryset.get(user=self.request.user)
            return profile
        except WorkerProfile.DoesNotExist:
            return Response({"message": "Worker profile not found."}, status=status.HTTP_404_NOT_FOUND)

class EmployerProfileVerifyAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            employer = EmployerProfile.objects.get(pk=pk)
            user = CustomUser.objects.get(pk=employer.user.pk)
            data={
                'is_identity_verified': True, 
                'is_email_verified': True,
                'is_phone_verified': True
            }
            seriaializer = CustomUserSerializer(instance=user, data=data, partial=True, context={'request': self.request})
            if seriaializer.is_valid():
                seriaializer.save()
                return Response({'status':'verified'}, status=status.HTTP_200_OK)
            return Response(seriaializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerProfile.DoesNotExist:
            return Response({'error': 'Employer not found'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'errorss': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkerProfileVerifyAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class= CustomUserSerializer

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            worker = WorkerProfile.objects.get(pk=pk)
            user = CustomUser.objects.get(pk=worker.user.pk)
            data={
                'is_identity_verified': True, 
                'is_email_verified': True,
                'is_phone_verified': True
            }
            seriaializer = CustomUserSerializer(instance=user, data=data, partial=True, context={'request': self.request})
            if seriaializer.is_valid():
                seriaializer.save()
                return Response({'status':'verified'}, status=status.HTTP_200_OK)
            return Response(seriaializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WorkerProfile.DoesNotExist:
            return Response({'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)