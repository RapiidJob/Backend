from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Messages
from .serializers import MessagesSerializer
from rest_framework import permissions
from RapidJob.permissions import IsSenderOrReadOnly

class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = [permissions.IsAuthenticated, IsSenderOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(sender=self.request.user)
        except Exception as e:
            return Response({"message": "An error occurred while creating the message", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
