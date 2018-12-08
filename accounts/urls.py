from django.urls import path
from . import views



urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('user_login/patient', views.patient, name='patient'),
    path('user_login/surgeon', views.surgeon, name='surgeon'),
    path('user_login/practice', views.practice, name='practice'),
    path('user_login/filter_user', views.filter_user, name='filter_user'), 
    # the above url does not get displayed ever
    # it is just present so that we can use the filter_user function from the views.py of the accounts app
    path('signup/surgeon', views.register_surgeon, name='signup_surgeon'),
    path('signup/patient', views.register_patient, name='signup_patient'),
]