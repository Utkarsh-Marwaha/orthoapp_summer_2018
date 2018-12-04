from django.urls import path
from first_app import views

app_name = 'first_app'

urlpatterns = [
    # path('', views.index, name='index'),
    path('welcome_to_orthoapp/', views.welcome_to_orthoapp, name='welcome_to_orthoapp'),
    path('before_your_surgery/', views.before_your_surgery, name='before_your_surgery'),
    path('register/', views.register, name = 'register'),
    path('user_login/', views.user_login, name = 'user_login'),
]
