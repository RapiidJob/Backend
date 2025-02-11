from django.db import models



class JobAddress(models.Model):
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    kebele = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_permanent = models.BooleanField(default=True)

    def __str__(self):
        strrep = self.country
        if self.region:
            strrep += " " + self.region
        if self.city:
            strrep += " " + self.city
        if self.kebele:
            strrep += " " + self.kebele
        if self.house_number:
            strrep += " " + self.house_number
        return strrep

class JobPostPhoto(models.Model):
    image = models.ImageField(upload_to='job_post_photos')

class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class JobSubcategory(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
PRICE_CHOICES = (
        ("Birr", "Birr"), ("USD", "USD")
    )
PAYEMENT_CHOICES = (
    ("PerHour", "PerHour"), ("PerDay", "PerDay"), ("PerWeek", "PerWeek"), ("PerMonth", "PerMonth"), ("PerTask", "PerTask"),
)

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subcategory = models.ForeignKey(JobSubcategory, on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    posted_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    payement_choice = models.CharField(choices=PAYEMENT_CHOICES, max_length=20, default="PerTask")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_price = models.FloatField(null=True)
    currency_type = models.CharField(choices=PRICE_CHOICES, max_length=20, default="Birr")
    job_address = models.ForeignKey(JobAddress, on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    post_photos = models.ManyToManyField(JobPostPhoto, related_name='jobs')
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        
        return "job_" + str(self.id) + " " + self.title


class UserSavedJob(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_jobs')
    created_at = models.DateTimeField(auto_now_add=True)