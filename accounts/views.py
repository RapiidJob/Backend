from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, EmployerProfile, WorkerProfile
from .serializers import CustomUserRegisterSerializer, EmployerProfileSerializer, WorkerProfileSerializer, LoginSerializer, CustomUserSerializer

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
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
