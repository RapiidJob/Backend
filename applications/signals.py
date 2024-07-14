# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Application, WorkInProgress, WorkHistory

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

        ### change the started_at feild of work in progress to when the application is accepted!
        if instance.APPLICATION_STATUS == 'Accepted':
            try:
                obj = WorkInProgress.filter(Application=instance)
                obj.started_at = timezone.now
                obj.save()
            except:
                pass

@receiver(post_save, sender=WorkInProgress)
def generate_work_history(sender, instance, created, **kwargs):
    if not created and instance.is_finished == True:
        application = instance.application

        work_history, created = WorkHistory.objects.get_or_create(
            job = instance.job,
            worker = application.worker,
            application=application,
            defaults={
                'paid_price': application.agreed_price,
                'currency_type': application.currency_type,
                'score': 0, # not sure what to put here
                'was_paid': True,
                'description': f'Job:{instance.job.title}\nEmployer: {instance.job.postd_by}\nWorker: {application.worker}\nStatus: Complete!'
            }
        )
        
        work_history.save()
