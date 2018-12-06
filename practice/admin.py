from django.contrib import admin
from .models import Practice


class PracticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    list_per_page = 10
    
# Register your models here.
admin.site.register(Practice, PracticeAdmin)