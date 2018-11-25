from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import Welcome_To_Orthoapp, Before_Your_Surgery

# Create your views here.
def index(request):
    my_dict = {'insert_me': "I am from views.py"}
    return render(request, 'first_app/index.html', context= my_dict)

def welcome_to_orthoapp(request):
    lis = Welcome_To_Orthoapp.objects.all()
    welcome_to_ortho_page = {'welcome_to_ortho_page': lis}
    return render(request, 'first_app/welcome_to_orthoapp.html', context = welcome_to_ortho_page)

def before_your_surgery(request):
    lis = Before_Your_Surgery.objects.all()
    before_your_surgery_page = {'before_your_surgery_page': lis}
    return render(request, 'first_app/before_your_surgery.html', context = before_your_surgery_page)
