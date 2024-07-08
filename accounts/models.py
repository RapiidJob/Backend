from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#import TimeStampedModel

from django.db import models
from jobs.models import JobCategory
from RapidJob.Abstractmodels import TimestampModel


class UserAddress(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    kebele = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_permanent = models.BooleanField(default=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    VERIFICATION_CHOICES = (
        ("NationalId", "NationalId"),
        ("Passport", "Passport"),
        ("KebeleId", "KebeleId"),
        ("DriversLicense", "DriversLicense"),
        ("SchoolId", "SchoolId"),
    )
    ACCOUNT_CHOICES = (
        ("Worker", "Worker"), ("Employer", "Employer"),( "Admin", "Admin")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_CHOICES, default="Worker")
    
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_identity_verified = models.BooleanField(default=False)
    
    verification_type = models.CharField(max_length=100, choices=VERIFICATION_CHOICES, null=True, blank=True)
    verification_document = models.FileField(upload_to='verification_documents', null=True, blank=True)
    rating  = models.IntegerField(default=0)
    
    is_email_verified = models.BooleanField(default=False, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False, null=True, blank=True)
    
    address = models.OneToOneField(UserAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='address_user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class WorkerProfile(models.Model):
    PLAN_CHOICES = (
        ('Free', 'Free'),
        ("Premium", "Premium"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='worker_profile')
    plan = models.CharField(max_length=100, choices=PLAN_CHOICES, default='Free')
    prefered_job_categories = models.ManyToManyField(JobCategory, related_name='job_categories')
    last_applied = models.DateTimeField(null=True, blank=True)
    last_paid = models.DateTimeField(null=True, blank=True)
    
class EmployerProfile(models.Model):
    PLAN_CHOICES = (
        ("Normal", "Normal"),
        ("Premium", "Premium"),
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    plan = models.CharField(max_length=100, choices=PLAN_CHOICES, default='Normal')
    last_paid = models.DateTimeField(null=True, blank=True)