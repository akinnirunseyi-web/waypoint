from django.contrib import admin
from trails.models import Trail, Park


class TrailInline(admin.TabularInline):
    """
    Inline admin for trails, allows managing trails
    directly from the Park admin page.
    """
    model  = Trail
    extra  = 1


class ParkAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Park model.
    Shows trails inline so parks and their trails
    can be managed from one page.
    """
    list_display  = ["name", "region"]
    search_fields = ["name", "region"]
    inlines       = [TrailInline]


class TrailAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Trail model.
    Shows key fields in the list view and enables search.
    """
    list_display  = ["name", "distance_km", "elevation_gain",
                     "difficulty", "is_open", "park", "added"]
    search_fields = ["name", "difficulty"]
    list_filter   = ["difficulty", "is_open", "park"]


admin.site.register(Park, ParkAdmin)
admin.site.register(Trail, TrailAdmin)