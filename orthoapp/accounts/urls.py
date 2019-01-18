from django.urls import path
from . import views



urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_login/patient', views.patient, name='patient'),
    path('user_login/surgeon', views.surgeon, name='surgeon'),
    path('user_login/practice', views.practice, name='practice'),
    path('user_login/filter_user', views.filter_user, name='filter_user'),
    path('user_login/change_password', views.change_password, name='change_password'),
    path('user_login/user_settings', views.user_settings, name='user_settings'),

    # the above url does not get displayed ever
    # it is just present so that we can use the filter_user function from the views.py of the accounts app
    path('signup/surgeon', views.register_surgeon, name='signup_surgeon'),
    path('signup/patient', views.register_patient, name='signup_patient'),
    path('signup/operation', views.register_operation, name='register_operation'),
]
