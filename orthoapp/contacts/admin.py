from django.contrib import admin
from . models import Contact
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('info_page_id','name','info_page', 'email', 'contact_date')
    list_display_links = ('info_page_id', 'name')
    search_fields = ('name', 'email', 'info_page')
    list_per_page = 25 

admin.site.register(Contact, ContactAdmin)