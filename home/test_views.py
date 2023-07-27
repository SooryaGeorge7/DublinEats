

# Create your tests here.
import os
from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.contrib.auth.models import User
from users.models import Profile
from review.models import Review, Restaurant


GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")


class TestSearchResultsViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testing@user.com", password="test123"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            website="Test website",
            address="test user address 07, Dublin",
            RestaurantId="c454h5",
        )
        self.review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
        )
        self.profile.pinned_restaurants.add(self.restaurant)
        self.profile.reviewed.add(self.restaurant)
    def test_searchresults_restaurants(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("searchresults"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/results.html")