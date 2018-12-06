from django.contrib import admin
from .models import Information_Page

class Information_PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','is_key_link','is_published','surgery_stage')
    list_display_links = ('id', 'title')
    list_filter = ('surgery_stage','is_key_link','is_published')
    list_editable = ('is_key_link','is_published')
    search_fields = ('title', 'description', 'surgery_stage')
    list_per_page = 10

# Register your models here.
admin.site.register(Information_Page, Information_PageAdmin)