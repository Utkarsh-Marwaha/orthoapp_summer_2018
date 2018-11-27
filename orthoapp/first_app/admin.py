from django.contrib import admin

from first_app.models import Person, Surgeon, Patient, DataPoint, StepCounter, KneeMotionRange, PainLevel, Operation, Appointment, UserProfileInfo

#importing static models
from first_app.models import Welcome_To_Orthoapp, Before_Your_Surgery
# Register your models here.
# admin.site.register(Person)
admin.site.register(Surgeon)
admin.site.register(Patient)
# admin.site.register(DataPoint)
admin.site.register(StepCounter)
admin.site.register(KneeMotionRange)
admin.site.register(PainLevel)
admin.site.register(Operation)
admin.site.register(Appointment)
admin.site.register(Welcome_To_Orthoapp)
admin.site.register(Before_Your_Surgery)
admin.site.register(UserProfileInfo)
