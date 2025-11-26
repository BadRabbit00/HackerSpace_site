from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'host', 'price')
    list_filter = ('date', 'required_plan')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    autocomplete_fields = ['host', 'participants']

