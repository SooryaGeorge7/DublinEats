from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_on = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    Rating = (
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent')
    )

    taste = models.IntegerField(choices=Rating)
    ambience = models.IntegerField(choices=Rating)
    customer_service = models.IntegerField(choices=Rating)
    location = models.IntegerField(choices=Rating)
    value_for_money = models.IntegerField(choices=Rating)

    def __str__(self):
        return f"{self.restaurant.name} - {self.user.username}'s Ratings"

