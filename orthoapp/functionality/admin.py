from django.contrib import admin
from .models import StepCounter, KneeMotionRange, PainLevel, Appointment

# Register your models here.

admin.site.register(StepCounter)
admin.site.register(KneeMotionRange)
admin.site.register(PainLevel)
admin.site.register(Appointment)