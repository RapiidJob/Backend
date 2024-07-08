from rest_framework import viewsets
from .models import CustomUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import EmployerProfileSerializer, WorkerProfileSerializer
from .models import EmployerProfile, WorkerProfile
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

def password_reset_confirm_view(request, uid, token):
    return render(request, 'password_reset_confirm.html', {'uid': uid, 'token': token})




class EmployerProfileCreateAPIView(generics.CreateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request: Request, *args, **kwargs):
        print("here")
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EmployerProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]

class WorkerProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = WorkerProfileSerializer
    permission_classes = [IsAuthenticated]

class WorkerProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = WorkerProfile.objects.all()
    serializer_class = WorkerProfileSerializer
    permission_classes = [IsAuthenticated]