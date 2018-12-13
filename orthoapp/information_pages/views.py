from django.shortcuts import render, get_object_or_404
from .models import Information_Page
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import surgery_stage_choices, hospital_name_choices

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
    
    information_page = get_object_or_404(Information_Page, pk=information_page_id)

    context = {
        'information_page' : information_page
    }

    return render (request, 'information_pages/information_page.html', context)

def search(request):

    queryset_list = Information_Page.objects.filter(is_published=True)

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # Surgery_Stage
    if 'city' in request.GET:
        surgery_stage = request.GET['city']
        if surgery_stage:
            queryset_list = queryset_list.filter(surgery_stage__iexact=surgery_stage)


    # Hospital
    if 'state' in request.GET:
        hospital_name = request.GET['state']
        if hospital_name:
            queryset_list = queryset_list.filter(hospital_name__iexact=hospital_name)

    context = {
        'surgery_stage_choices' : surgery_stage_choices,
        'hospital_name_choices' : hospital_name_choices,
        'info_pages'            : queryset_list
    }
    return render (request, 'information_pages/search.html', context)