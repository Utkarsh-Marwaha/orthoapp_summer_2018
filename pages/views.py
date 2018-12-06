from django.shortcuts import render
from django.http import HttpResponse

from information_pages.models import Information_Page
from practice.models import Practice

# Create your views here.
def index (request):
    info_pages = Information_Page.objects.all().filter(is_published = True, is_key_link = True)[:3]

    context = {
        'info_pages' : info_pages
    }

    return render(request, 'pages/index.html', context)

def about (request):
    # Get all team-members
    team_members = Practice.objects.all();

    #Get the team member who will be handling the inquiries about pages
    lead_contacts = Practice.objects.all().filter(is_lead_contact= True)

    context = {
        'team_members'  : team_members,
        'lead_contacts' : lead_contacts
    }
    return render(request, 'pages/about.html', context)