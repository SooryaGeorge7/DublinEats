from django.urls import path
from . import views

urlpatterns = [
    path(
        "asian/",
        views.restaurants,
        {"category": "asian"},
        name="asian",
    ),
    path(
        "european/",
        views.restaurants,
        {"category": "european"},
        name="european",
        
    ),
    path(
        "african/",
        views.restaurants,
        {"category": "african"},
        name="african",
    ),
    path(
        "irish/",
        views.restaurants,
        {"category": "irish"},
        name="irish",
    ),
    path(
        "american/",
        views.restaurants,
        {"category": "american"},
        name="american",
    ),
    path(
        "all/",
        views.restaurants,
        {"category": "all"},
        name="all-restaurants",
    ),
    path(
        "to_visit/<str:restaurant_id>/",
        views.to_visit,
        name="to_visit",
    ),
    path(
        "remove_pin/<str:restaurant_id>/",
        views.remove_pin,
        name="remove_pin",
    ),
    


]
