from django.contrib import admin

from .models import CustomUser, WorkerProfile, EmployerProfile, UserAddress

admin.site.register(CustomUser)
admin.site.register(WorkerProfile)
admin.site.register(EmployerProfile)
admin.site.register(UserAddress)