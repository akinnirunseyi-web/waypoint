from django.contrib import admin
from trails.models import Trail


class TrailAdmin(admin.ModelAdmin):
    """
    Admin configuration for Trail model.
    
    """
    list_display  = ["name", "distance_km", "elevation_gain", "difficulty", "is_open", "added"]
    search_fields = ["name", "difficulty"]
    list_filter   = ["difficulty", "is_open"]


admin.site.register(Trail, TrailAdmin)