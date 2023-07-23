from django.test import TestCase
from django.contrib.auth.models import User
from review.models import Restaurant
from .models import Profile, placeholder


class TestProfileModel(TestCase):
    

    def setUp(self):
        
        self.restaurant = Restaurant.objects.create(
            name="testRestaurant",
            website="testingwebsite@info.com",
            address="Tester123",
            RestaurantId="test1467",
        )
        self.user = User.objects.create_user(
            username="testuser", email="user@testing.com", password="test123"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.firstname = "Soorya"
        self.profile.surname = "George"
        self.profile.about = "Foodie till i die!"
        self.profile.profile_image =  placeholder
        self.profile.fav_food = "Indian"
        self.profile.pinned_restaurants.add(self.restaurant)
        self.profile.reviewed.add(self.restaurant)
        self.profile.pinned_restaurants.remove(self.restaurant)
        self.profile.reviewed.remove(self.restaurant)

    def test_profile_model(self):
        
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.firstname, "Soorya")
        self.assertEqual(self.profile.surname, "George")
        self.assertEqual(self.profile.about, "Foodie till i die!")
        self.assertEqual(self.profile.profile_image, placeholder)
        self.assertEqual(self.profile.fav_food, "Indian")
        
    def test_pinned_restaurants_and_reviewed_relationships(self):
        
        restaurant1 = Restaurant.objects.create(
            name="Restaurant1",
            website="Restaurant1website@info.com",
            address="Restaurant1, Dublin",
            RestaurantId="Rest1423",
            )
        restaurant2 = Restaurant.objects.create(
            name="Restaurant2",
            website="Restaurant2website@info.com",
            address="Restaurant2, Dublin",
            RestaurantId="Rest4353",
        )

        profile = self.profile

        profile.pinned_restaurants.add(restaurant1)
        profile.pinned_restaurants.add(restaurant2)

        
        self.assertTrue(profile.pinned_restaurants.filter(name="Restaurant1").exists())
        self.assertTrue(profile.pinned_restaurants.filter(name="Restaurant2").exists())