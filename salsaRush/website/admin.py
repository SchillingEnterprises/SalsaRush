from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date_time", "location", "organizer")
    list_filter = ("date_time",)
    search_fields = ("title", "description", "location")
    ordering = ("date_time",)
    date_hierarchy = "date_time"
