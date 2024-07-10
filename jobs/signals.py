# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Job
from accounts.models import CustomUser 
import json

@receiver(post_save, sender=Job)
def job_created(sender, instance, created, **kwargs):
    if created:
        similar_users = find_similar_users(instance.job_address)

        channel_layer = get_channel_layer()
        for user in similar_users:
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "job.notification",
                    "message": json.dumps({
                        "job_id": instance.id,
                        "title": instance.title,
                        "description": instance.description,
                    })
                }
            )

def find_similar_users(job_address):
    #will be added other criterias
    return CustomUser.objects.filter(address__city=job_address.city)
