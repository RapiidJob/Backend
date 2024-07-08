from rest_framework import serializers
from .models import Messages

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['id', 'sender', 'receiver', 'job', 'text', 'created_at', 'is_seen']
