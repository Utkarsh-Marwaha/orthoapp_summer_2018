from django.contrib import admin
from .models import Information_Page

""" This admin.py file is used to register/display the models defined
     within the accounts app on the admin panel in the backend """


class Information_PageAdmin(admin.ModelAdmin):
    list_display       = ('id', 'title','is_key_link','is_published','surgery_stage')
    list_display_links = ('id', 'title')
    list_filter        = ('surgery_stage','is_key_link','is_published')
    list_editable      = ('is_key_link','is_published')
    search_fields      = ('title', 'description', 'surgery_stage')
    list_per_page      = 10

    def get_queryset(self, request):
        queryset = super(Information_PageAdmin, self).get_queryset(request)
        queryset = queryset.order_by('id')
        return queryset

# register the Information_Page model so that it is visible on the admin panel in the backend
admin.site.register(Information_Page, Information_PageAdmin)
