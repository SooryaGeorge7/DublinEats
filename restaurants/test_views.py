
import os
from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.contrib.auth.models import User
from users.models import Profile
from review.models import Review, Restaurant


GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")


class TestRestaurantViews(TestCase):

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

    def test_asian_restaurants(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("asian"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/categories.html")

    def test_european_restaurants(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("european"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/categories.html")

    def test_african_restaurants(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("african"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/categories.html")

    def test_irish_restaurants(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("irish"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/categories.html")

    def test_american_restaurants(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("european"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurants/categories.html")

    def test_add_restaurant_to_pinnedrestaurants(self):
        
        self.profile.pinned_restaurants.clear()
        self.client.login(username="testuser", password="test123")
        response = self.client.get(
            reverse("to_visit", kwargs={"restaurant_id": self.restaurant.RestaurantId})
        )
        self.assertEqual(response.status_code, 302)

    def test_remove_restaurant_from_to_pinnedrestaurants(self):
        
        self.client.login(username="testuser", password="test123")
        response = self.client.get(
            reverse("to_visit", kwargs={"restaurant_id": self.restaurant.RestaurantId})
        )
        self.assertFalse(self.restaurant in self.profile.pinned_restaurants.all())

    def test_remove_restaurant_from_profile_page(self):
       
        self.client.login(username="testuser", password="test123")
        response = self.client.get(
            reverse("remove_pin", kwargs={"restaurant_id": self.restaurant.RestaurantId})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.restaurant in self.profile.pinned_restaurants.all())

    def test_edit_review_from_profile_page_reviews(self):
        self.client.login(username="testuser", password="test123")
        review = Review.objects.get(user=self.user, restaurant=self.restaurant)

        if review:
            if self.restaurant in self.profile.reviewed.all():
                return reverse(
                    "edit_review", args=[self.restaurant.RestaurantId, review.id]
                )
