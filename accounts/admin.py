from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Surgeon, Patient, Practice, DataPoint, StepCounter, KneeMotionRange, PainLevel, Operation, Appointment, UserProfileInfo


admin.site.register(MyUser, UserAdmin)
admin.site.register(Surgeon)
admin.site.register(Patient)
admin.site.register(Practice)

admin.site.register(StepCounter)
admin.site.register(KneeMotionRange)
admin.site.register(PainLevel)
admin.site.register(Operation)
admin.site.register(Appointment)
