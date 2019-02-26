from django.contrib import admin
from .models import StepCounter, KneeMotionRange, PainLevel, Appointment

""" This admin.py file is used to register/display the models defined
     within the functionality app on the admin panel in the backend"""
     
# register the StepCounter model so that it is visible on the admin panel in the backend
admin.site.register(StepCounter)

# register the KneeMotionRange model so that it is visible on the admin panel in the backend
admin.site.register(KneeMotionRange)

# register the PainLevel model so that it is visible on the admin panel in the backend
admin.site.register(PainLevel)

# register the Appointment model so that it is visible on the admin panel in the backend
admin.site.register(Appointment)