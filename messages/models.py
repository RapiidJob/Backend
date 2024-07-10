from django.db import models
from accounts.models import CustomUser
from jobs.models import Job
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer


User = get_user_model()

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name="job_messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)