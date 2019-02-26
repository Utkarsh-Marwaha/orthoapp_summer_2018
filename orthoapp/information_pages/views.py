from django.shortcuts import render, get_object_or_404
from .models import Information_Page
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import surgery_stage_choices, hospital_name_choices


def index (request):

    # Fetch all the information pages from the backend which are published and order them by their title
    info_pages = Information_Page.objects.all().filter(is_published = True).order_by('title')

    # add pagination (6 per page)
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

"""This function allows us to search the information pages based on keywords in the main text, hospital name or the surgery stage"""
def search(request):

    queryset_list = Information_Page.objects.filter(is_published=True).order_by('title')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(main_text__icontains=keywords).order_by('title')

    # Surgery_Stage
    if 'city' in request.GET:
        surgery_stage = request.GET['city']
        if surgery_stage:
            queryset_list = queryset_list.filter(surgery_stage__iexact=surgery_stage).order_by('title')


    # Hospital
    if 'state' in request.GET:
        hospital_name = request.GET['state']
        if hospital_name:
            queryset_list = queryset_list.filter(hospital_name__iexact=hospital_name).order_by('title')

    context = {
        'surgery_stage_choices' : surgery_stage_choices,
        'hospital_name_choices' : hospital_name_choices,
        'info_pages'            : queryset_list
    }
    return render (request, 'information_pages/search.html', context)
