from django.shortcuts import render
from .models import Information_Page
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def index (request):

    info_pages = Information_Page.objects.all().filter(is_published = True)

    paginator = Paginator(info_pages, 6)
    page = request.GET.get('page')
    paged_info_pages = paginator.get_page(page)

    context = {
        'info_pages' : paged_info_pages
    }
    return render (request, 'information_pages/information_pages.html', context)

def information_page(request, information_page_id):
    return render (request, 'information_pages/information_page.html')

def search(request):
    return render (request, 'information_pages/search.html')