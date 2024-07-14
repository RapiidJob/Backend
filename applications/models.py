from django.db import models
from accounts.models import CustomUser
from jobs.models import Job
from django.utils import timezone


PRICE_CHOICES = (
        ("Birr", "Birr"), ("USD", "USD")
    )
class Application(models.Model):
    APPLICATION_STATUS = (
        ("NotSeen", "Not seen"), ("Seen", "Seen"), ("Accepted", "Accepted"), ("Rejected", "Rejected")
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_applications')
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='worker_applications')
    application_letter = models.TextField(null=True, blank=True)
    application_date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=APPLICATION_STATUS, default="NotSeen")
    agreed_price = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=PRICE_CHOICES, default="Birr")
    
class WorkHistory(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_applications')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    paid_price = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=PRICE_CHOICES,default="Birr")
    score = models.PositiveIntegerField(default = 0)
    was_paid = models.BooleanField(default=False)

class WorkInProgress(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='jobs')
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='applications')
    started_at = models.DateTimeField(default=timezone.now)
    is_finished = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Current job in progress: " + str(self.job.title)
    