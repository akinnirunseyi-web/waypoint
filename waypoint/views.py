from django.shortcuts import render


def home(request):
    """
    Renders the homepage with a welcome message.

    Parameters:
    request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: Renders home.html with greeting context variable.
    """
    context = {
        "greeting": "I Welcome you to Waypoint — your trail finder and trip planner!"
    }
    return render(request, "home.html", context)


def report(request):
    """
    Handles the trail report form.
    GET  — it will render a blank report form.
    POST — it will read submitted data and renders a thank-you page.

    Parameters:
    request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: Renders report.html on GET, thankyou.html on POST.
    """
    if request.method == "POST":
        name       = request.POST.get("name", "")
        email      = request.POST.get("email", "")
        trail_name = request.POST.get("trail", "")
        note       = request.POST.get("note", "")
        context = {
            "name":       name,
            "email":      email,
            "trail_name": trail_name,
            "note":       note,
        }
        return render(request, "thankyou.html", context)

    return render(request, "report.html")


def search(request):
    """
    Handles trail search by reading a query parameter from the URL.
    Safely returns an empty string if no query is provided.

    Parameters:
    request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: Renders search.html with the query context variable.
    """
    query = request.GET.get("q", "")
    context = {
        "query": query,
    }
    return render(request, "search.html", context)

def catalog(request):
    """
    Renders the trail catalog page with a hardcoded list of trails.

    Parameters:
    request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: Renders catalog.html with a list of trail dictionaries.
    """
    trails = [
        {"name": "Maple Ridge Trail",     "distance": 12.4, "elevation": 400,  "difficulty": "moderate", "is_open": True},
        {"name": "Summit Peak Route",     "distance": 8.7,  "elevation": 950,  "difficulty": "expert",   "is_open": True},
        {"name": "Riverside Walk",        "distance": 5.2,  "elevation": 80,   "difficulty": "easy",     "is_open": True},
        {"name": "Wilderness Loop",       "distance": 34.0, "elevation": 1800, "difficulty": "expert",   "is_open": False},
        {"name": "Cedar Valley Path",     "distance": 9.1,  "elevation": 310,  "difficulty": "moderate", "is_open": True},
        {"name": "Blue Ridge Sprint",     "distance": 6.5,  "elevation": 220,  "difficulty": "easy",     "is_open": False},
        {"name": "Granite Peak Traverse", "distance": 18.3, "elevation": 1200, "difficulty": "hard",     "is_open": True},
    ]
    context = {"trails": trails}
    return render(request, "catalog.html", context)