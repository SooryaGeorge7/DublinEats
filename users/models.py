from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from review.models import Restaurant
# Create your models here.

placeholder= (f"https://res.cloudinary.com/dif9bjzee/image/upload/c_scale,h_50,w_50/v1689590568/profile-gda8c660e4_640_z54qoi.webp")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(
        max_length=50, null=True, blank=True, default="Firstname"
    )
    surname = models.CharField(
        max_length=50, null=True, blank=True, default="Surname"
    )
    about = models.TextField(null=True,
        blank=True,
        max_length=200,
        default="Foodie in and out..!",)
    
    profile_image = CloudinaryField(
        "image",
        default = placeholder,
        eager=[{"width": 50, "height": 50, "crop": "crop"}],
        transformation={
            "width": 50,
            "height": 50,
            "crop": "fill",
        },
        blank= True,
        null= True,
    )
    fav_food = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default="What's your favourite cuizine?",
    )
    
    pinned_restaurants = models.ManyToManyField(
        Restaurant, related_name="to_visit", blank=True
    )
    reviewed = models.ManyToManyField(
        Restaurant, related_name="reviewed", blank=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'