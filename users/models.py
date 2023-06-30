from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.

placeholder= (f"https://res.cloudinary.com/dif9bjzee/image/upload/v1688077403/restaurant_pbldeh.png")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField(
        "profile_images",
        default = placeholder,
        transformation={
            "width": 50,
            "height": 50,
            "crop": "fill",
        },
        blank= True,
        null= True,
    )

    def __str__(self):
        return f'{self.user.username} Profile'