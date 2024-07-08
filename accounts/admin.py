from django.contrib import admin

from .models import CustomUser, WorkerProfile, EmployerProfile

admin.site.register(CustomUser)
admin.site.register(WorkerProfile)
admin.site.register(EmployerProfile)