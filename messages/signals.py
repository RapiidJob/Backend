from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Messages
from accounts.models import CustomUser

@receiver(post_save, sender=Messages)
def send_message_email(sender, instance, created, **kwargs):
    if created and instance.sender.account_type == 'employer' and instance.receiver.account_type == 'worker':
        subject = f"New Message from {instance.sender.username}"
        message = f"You have a new message regarding job {instance.job.title}. Check it out!"
        recipient_email = instance.receiver.email
        send_mail(subject, message, None, [recipient_email])
