from django.contrib import admin
from . models import Contact

""" This admin.py file is used to register/display the models defined
     within the accounts app on the admin panel in the backend"""


class ContactAdmin(admin.ModelAdmin):

    """
    The list_display (here) is a tuple of field names. If set instead of being the view 
    a single list, that list can be turned into a table! And in that case list_display the 
    fields to be columns of such table.
    """
    list_display       = ('info_page_id','name','info_page', 'email', 'contact_date')
    list_display_links = ('info_page_id', 'name')
    
    """
    The search_fields (here), is a list of “QuerySet” fields, that can be used to filter search your result set.
    """
    search_fields      = ('name', 'email', 'info_page')

    """
    Set list_per_page to control how many items appear on each paginated admin change list page. By default, this is set to 100.
    """
    list_per_page      = 10 

# register the Surgeon model so that it is visible on the admin panel in the backend
admin.site.register(Contact, ContactAdmin)
