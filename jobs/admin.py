from django.contrib import admin

from .models import Job, JobCategory, JobSubcategory, JobAddress, JobPostPhoto


admin.site.register(Job)
admin.site.register(JobSubcategory)
admin.site.register(JobCategory)
admin.site.register(JobAddress)
admin.site.register(JobPostPhoto)