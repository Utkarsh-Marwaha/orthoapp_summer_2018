from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('user_login/',                 views.user_login,      name='user_login'),
    path('user_logout/',                views.user_logout,     name='user_logout'),

    # These urls are for user dashboards
    path('user_login/patient',                  views.patient,         name='patient'),
    path('user_login/surgeon',                  views.surgeon,         name='surgeon'),
    path('user_login/practice',                 views.practice,        name='practice'),

    #This url is present so that we can use the filter_user function from the views.py of the accounts app
    path('user_login/filter_user',      views.filter_user,     name='filter_user'),
    path('user_login/change_password',  views.change_password, name='change_password'),
    path('user_login/user_settings',    views.user_settings,   name='user_settings'),


    # password reset
    path('password-reset/',
    auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
    name='password_reset'),

    # password reset done
    path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
    name='password_reset_done'),

    # password reset confirmation
    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
    name='password_reset_confirm'),

    # password reset complete
    path('password-reset/complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
    name='password_reset_complete'),

    # These urls are for user registrations
    path('signup/surgeon',      views.register_surgeon,     name='signup_surgeon'),
    path('signup/patient',      views.register_patient,     name='signup_patient'),
    path('signup/operation',    views.register_operation,   name='register_operation'),
]
