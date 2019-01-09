from django.urls import path
from . import views # helps us import all the views of this app



urlpatterns = [
    path('stepcounter/', views.stepcounter, name='stepcounter'),
    path('kneemotionrange/', views.kneemotionrange, name='kneemotionrange'),
    path('painlevel/', views.painlevel, name='painlevel'),
    path('record', views.Record.as_view(), name='record'),
    path('record/data', views.RecordData.as_view()),

]
