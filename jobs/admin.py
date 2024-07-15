from django.contrib import admin

from .models import Job, JobCategory, JobSubcategory, JobAddress, JobPostPhoto, UserSavedJob

admin.site.register(UserSavedJob)
admin.site.register(Job)
admin.site.register(JobSubcategory)
admin.site.register(JobCategory)
admin.site.register(JobAddress)
admin.site.register(JobPostPhoto)