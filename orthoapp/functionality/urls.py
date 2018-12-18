from django.urls import path
from . import views



urlpatterns = [
    path('stepcounter/', views.stepcounter, name='stepcounter'),
    path('kneemotionrange/', views.kneemotionrange, name='kneemotionrange'),
    path('painlevel/', views.painlevel, name='painlevel'),

]
