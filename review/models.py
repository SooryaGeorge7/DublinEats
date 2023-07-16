from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=300)
    website = models.URLField(blank=True)
    address = models.TextField()
    RestaurantId = models.CharField(
        max_length=300, null=True, blank=True, unique=True
    )

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_on = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    Rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )

    taste = models.IntegerField(choices=Rating, default=0)
    ambience = models.IntegerField(choices=Rating, default=0)
    customer_service = models.IntegerField(choices=Rating, default=0)
    location = models.IntegerField(choices=Rating, default=0)
    value_for_money = models.IntegerField(choices=Rating, default=0)
    comment_text = models.TextField(null=False,
        blank=False,
        default="Type in a review here...",)

    def __str__(self):
        return f"{self.user.username}'s review of {self.restaurant.name}"

# class Comment(models.Model):
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment_text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.restaurant.name} - {self.user.username}'s Comment"