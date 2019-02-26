from django.shortcuts import render
from django.http import HttpResponse
from information_pages.choices import surgery_stage_choices, hospital_name_choices


from information_pages.models import Information_Page
from developer.models import Developer

def index (request):

    # Fetch all the information pages from the backend which are published and are key links. Order them by their title
    info_pages = Information_Page.objects.all().filter(is_published = True, is_key_link = True)[:3]

    context = {
        'info_pages'            : info_pages,
        'surgery_stage_choices' : surgery_stage_choices,
        'hospital_name_choices' : hospital_name_choices
    }

    return render(request, 'pages/index.html', context)

def about (request):
    # Get all team-members
    team_members = Developer.objects.all()

    #Get the team member who will be handling the inquiries about pages
    lead_contacts = Developer.objects.all().filter(is_lead_contact= True)

    context = {
        'team_members'  : team_members,
        'lead_contacts' : lead_contacts
    }
    return render(request, 'pages/about.html', context)