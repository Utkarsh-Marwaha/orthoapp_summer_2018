from django.urls import path
from . import views



urlpatterns = [
    path('stepcounter/', views.stepcounter, name='stepcounter'),
    path('kneemotion/', views.kneemotion, name='kneemotion'),
    path('painlevel/', views.painlevel, name='painlevel'),
    
]