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

    def save(self, *args, **kwargs):
        print("PRESAVE")
        super().save(*args, **kwargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{self.receiver.id}",
            {
                "type": "chat_message",
                "message": {
                    "id": self.id,
                    "sender": self.sender.id,
                    "receiver": self.receiver.id,
                    "text": self.text,
                    "created_at": self.created_at.isoformat(),
                    "is_seen": self.is_seen,
                }
            }
        )
