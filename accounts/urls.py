from django.urls import path
from . import views

urlpatterns = [
    path('user_login/', views.user_login, name = 'user_login'),
    path('signup/', views.SignUpView.as_view(), name = 'signup'),
    path('signup/surgeon', views.register_surgeon, name = 'signup_surgeon'),
    path('signup/patient', views.register_patient, name = 'signup_patient'),
]