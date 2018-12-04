from django.urls import path
from first_app import views

app_name = 'first_app'

urlpatterns = [
    # path('', views.index, name='index'),
    path('welcome_to_orthoapp/', views.welcome_to_orthoapp, name='welcome_to_orthoapp'),
    path('before_your_surgery/', views.before_your_surgery, name='before_your_surgery'),
    # path('register/', views.register, name = 'register'),
    path('user_login/', views.user_login, name = 'user_login'),
    path('signup/', views.SignUpView.as_view(), name = 'signup'),
    path('signup/surgeon', views.register_surgeon, name = 'signup_surgeon'),
    path('signup/patient', views.register_patient, name = 'signup_patient'),

]
