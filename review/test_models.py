from django.test import TestCase
from django.contrib.auth.models import User
from .models import Review, Restaurant

class TestRestaurantModel(TestCase):
    def setUp(self):
        Restaurant.objects.create(
            name="Test Restaurant",
            website="dublineatstest@info.com",
            address="07 Tester, Dublin",
            RestaurantId="test17",
            
        )

    def test_restaurant_model(self):
        restaurant = Restaurant.objects.get(name="Test Restaurant")
        self.assertEqual(restaurant.name, "Test Restaurant")
        self.assertEqual(restaurant.website, "dublineatstest@info.com")
        self.assertEqual(restaurant.address, "07 Tester, Dublin")
        self.assertEqual(restaurant.RestaurantId, "test17")

class TestReviewModel(TestCase):

    def setUp(self):
        
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            website="dublineatstest@info.com",
            address="07 Tester, Dublin",
            RestaurantId="test17",   
        )
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="test123"
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
        self.expected_str = str(f"{self.user.username}'s review of {self.restaurant.name}")

    def test_review_model(self):
        
        self.assertEqual(self.review.user.username, "testuser")
        self.assertEqual(self.review.restaurant.name, "Test Restaurant")
        self.assertEqual(self.review.taste, 3)
        self.assertEqual(self.review.ambience, 4)
        self.assertEqual(self.review.customer_service, 3)
        self.assertEqual(self.review.location, 4)
        self.assertEqual(self.review.value_for_money, 4)
        self.assertEqual(self.review.comment_text, "Love this restaurant")
        self.assertEqual(str(self.review), self.expected_str)