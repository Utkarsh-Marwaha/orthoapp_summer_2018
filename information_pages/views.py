from django.shortcuts import render

# Create your views here.
def index (request):
    return render (request, 'information_pages/information_pages.html')

def information_page(request):
    return render (request, 'information_pages/information_page.html')

def search(request):
    return render (request, 'information_pages/search.html')