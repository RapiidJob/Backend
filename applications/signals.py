# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Application

@receiver(post_save, sender=Application)
def send_application_status_email(sender, instance, created, **kwargs):
    if instance.status == "Accepted" and not created:
        worker_email = instance.worker.email
        job_title = instance.job.title

        subject = 'Your Application Status'
        html_message = render_to_string('email/application_accepted.html', {'job_title': job_title})
        plain_message = strip_tags(html_message)  # This is the plain text version of the email

        send_mail(
            subject,
            plain_message,
            'abdulwahidhussen10@gmail.com',  
            [worker_email],  
            html_message=html_message 
        )
