from django.shortcuts import render, get_object_or_404
from trails.models import Trail, Park


def catalog(request):
    """
    Renders the trail catalog from the database.
    Only shows open trails, ordered by distance.

    Parameters:
    request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: Renders catalog.html with open trails from the database.
    """
    trails = Trail.objects.filter(is_open=True).order_by("distance_km")
    context = {"trails": trails}
    return render(request, "catalog.html", context)


def park_detail(request, park_id):
    """
    Renders a page showing a specific park and all its trails.
    Uses the reverse ForeignKey relation (park.trails) to query
    trails belonging to that park.

    Parameters:
    request  (HttpRequest): The incoming HTTP request.
    park_id  (int):         The primary key of the park to display.

    Returns:
    HttpResponse: Renders park_detail.html with the park and its trails.
    """
    park   = get_object_or_404(Park, pk=park_id)
    trails = park.trails.all().order_by("distance_km")
    context = {
        "park":   park,
        "trails": trails,
    }
    return render(request, "park_detail.html", context)


def parks(request):
    """
    Renders a list of all parks.

    Parameters:
    request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: Renders parks.html with all parks.
    """
    all_parks = Park.objects.all()
    context   = {"parks": all_parks}
    return render(request, "parks.html", context)