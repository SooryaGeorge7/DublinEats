from django.urls import path
from . import views

urlpatterns = [
    path(
        "review/<str:restaurant_id>/",
        views.review,
        name="review",
    ),
    path(
        "allreviews/<str:restaurant_id>/",
        views.allreviews,
        name="allreviews",
    ),
]
