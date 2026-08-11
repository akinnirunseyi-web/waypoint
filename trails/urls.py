from django.urls import path
from trails import views

urlpatterns = [
    path("parks/",             views.parks,       name="parks"),
    path("parks/<int:park_id>/", views.park_detail, name="park-detail"),
]