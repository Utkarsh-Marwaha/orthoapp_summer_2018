from django.urls import path
from first_app import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('welcome_to_orthoapp/', views.welcome_to_orthoapp, name='welcome_to_orthoapp'),
    path('before_your_surgery/', views.before_your_surgery, name='before_your_surgery'),

]
