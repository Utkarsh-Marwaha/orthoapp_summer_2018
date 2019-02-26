from django.urls import path
from . import views

urlpatterns =[
    path('',                          views.index,            name='information_pages'),
    path('<int:information_page_id>', views.information_page, name= 'information_page'),
    path('search',                    views.search,           name='search'),
]