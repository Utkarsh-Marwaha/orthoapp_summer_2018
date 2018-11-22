from django.contrib import admin
from first_app.models import Person, Surgeon, Patient, DataPoint, StepCounter, KneeMotionRange, PainLevel
# Register your models here.
# admin.site.register(Person)
admin.site.register(Surgeon)
admin.site.register(Patient)
# admin.site.register(DataPoint)
admin.site.register(StepCounter)
admin.site.register(KneeMotionRange)
admin.site.register(PainLevel)
