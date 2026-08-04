from django.shortcuts import render
from trails.models import Trail


def catalog(request):
    """
    Renders the trail catalog from the database.
    Only shows open trails, ordered by distance.

    Parameters:
    request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: Renders catalog.html with trails from the database.
    """
    trails = Trail.objects.filter(is_open=True).order_by("distance_km")
    context = {"trails": trails}
    return render(request, "catalog.html", context)