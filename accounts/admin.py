from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Surgeon, Patient, Practice, Operation


admin.site.register(MyUser, UserAdmin)
admin.site.register(Surgeon)
admin.site.register(Patient)
admin.site.register(Practice)
admin.site.register(Operation)
