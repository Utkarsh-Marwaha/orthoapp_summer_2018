from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Surgeon, Patient, Practice, Operation



""" This admin.py file is used to register/display the models defined
     within the accounts app on the admin panel in the backend"""

""" Django uses UserAdmin to render a nice admin look for the default User model. 
    By just using the following statement in our admin.py-file, we can get the same
    look for our custom MyUser model. """
admin.site.register(MyUser, UserAdmin)

# register the Surgeon model so that it is visible on the admin panel in the backend
admin.site.register(Surgeon)

# register the Patient model so that it is visible on the admin panel in the backend
admin.site.register(Patient)

# register the Practice model so that it is visible on the admin panel in the backend
admin.site.register(Practice)

# register the Operation model so that it is visible on the admin panel in the backend
admin.site.register(Operation)
