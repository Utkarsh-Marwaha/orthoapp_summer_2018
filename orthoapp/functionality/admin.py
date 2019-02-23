from django.contrib import admin
from .models import StepCounter, KneeMotionRange, PainLevel, Appointment

""" This admin.py file is used to register/display the models defined
     within the functionality app on the admin panel in the backend"""

""" Django uses UserAdmin to render a nice admin look for the default User model. 
    By just using the following statement in our admin.py-file, we can get the same
    look for our custom MyUser model. """

# register the StepCounter model so that it is visible on the admin panel in the backend
admin.site.register(StepCounter)

# register the KneeMotionRange model so that it is visible on the admin panel in the backend
admin.site.register(KneeMotionRange)

# register the PainLevel model so that it is visible on the admin panel in the backend
admin.site.register(PainLevel)

# register the Appointment model so that it is visible on the admin panel in the backend
admin.site.register(Appointment)