import os
from django.test import TestCase, Client
from django.urls import reverse
import requests
from django.contrib.auth.models import User
from .models import Restaurant, Review
from users.models import Profile





class TestReviewViews(TestCase):
    def setUp(self):
        
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="test123"
        )
        self.profile = Profile.objects.get(user=self.user)
        restaurant_id = "chye750"
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            website="dublineatstest@info.com",
            address="07 Tester, Dublin",
            RestaurantId="test17",
        )

        self.review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            taste = 3,
            ambience = 4,
            customer_service = 3,
            location = 4,
            value_for_money = 4,
            comment_text = "Love this restaurant",
        )

        self.client.login(username="testuser", password="test123")

    def test_review_page_and_rating(self):
        
        response = self.client.get(
            reverse("review", args={self.restaurant.RestaurantId})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "review/review_page.html")

        review_data = {
            'taste': 3,
            'ambience': 4,
            'customer_service': 3,
            'value_for_money': 4,
            'location': 4,
            'comment_text':"Love this restaurant",
        }

        response = self.client.post(
            reverse("review", args={self.restaurant.RestaurantId}),
            data=review_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dublineats-home"))
        new_review = Review.objects.get(id=2)
        self.assertEqual(new_review.taste, 3)
        self.assertEqual(new_review.ambience, 4)
        self.assertEqual(new_review.customer_service, 3)
        self.assertEqual(new_review.location, 4)
        self.assertEqual(new_review.value_for_money, 4)
        self.assertEqual(new_review.comment_text, "Love this restaurant")
    def test_edit_review(self):
        response = self.client.get(
            reverse(
                "edit_review",
                kwargs={
                    "restaurant_id": self.restaurant.RestaurantId,
                    "review_id": self.review.id,
                },
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "review/review_page.html")
        self.assertEqual(self.review.taste, 3)
        self.assertEqual(self.review.ambience, 4)
        self.assertEqual(self.review.customer_service, 3)
        self.assertEqual(self.review.location, 4)
        self.assertEqual(self.review.value_for_money, 4)
        self.assertEqual(self.review.comment_text, "Love this restaurant")
        review_data = {
            'taste': 3,
            'ambience': 4,
            'customer_service': 3,
            'value_for_money': 4,
            'location': 4,
            'comment_text':"Love this restaurant",
        }

        response = self.client.post(
            reverse(
                "edit_review",
                kwargs={
                    "restaurant_id": self.restaurant.RestaurantId,
                    "review_id": self.review.id,
                },
            ),
            data=review_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("allreviews", kwargs={"restaurant_id": self.restaurant.RestaurantId}))

        updated_review = Review.objects.get(id=self.review.id)
        
        self.assertEqual(updated_review.taste, 3)
        self.assertEqual(updated_review.ambience, 4)
        self.assertEqual(updated_review.customer_service, 3)
        self.assertEqual(updated_review.location, 4)
        self.assertEqual(updated_review.value_for_money, 4)
        self.assertEqual(updated_review.comment_text, "Love this restaurant")

    def test_delete_review(self):
       
        review_count = Review.objects.all().count()
        self.assertEqual(review_count, 1)

        response = self.client.post(
            reverse(
                "delete_review",
                kwargs={
                    "restaurant_id": self.restaurant.RestaurantId,
                    "review_id": self.review.id,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("profile"))
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())
        new_review_count = Review.objects.all().count()
        self.assertEqual(new_review_count, 0)

   