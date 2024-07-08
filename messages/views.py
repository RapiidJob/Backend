from rest_framework import viewsets
from .models import Messages
from .serializers import MessagesSerializer
from rest_framework import permissions
from RapidJob.permissions import IsSenderOrReadOnly

class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    permission_classes = [permissions.IsAuthenticated, IsSenderOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)