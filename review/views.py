from django.shortcuts import render, redirect
from .forms import RatingForm, CommentForm
from .models import Restaurant, Reviews, Comment

def review(request, restaurant_id):
    restaurant = Restaurant.objects.get(RestaurantId= restaurant_id)
    ratings = Reviews.objects.filter(restaurant=restaurant)
    comments = Comment.objects.filter(restaurant=restaurant)
    rating_form = RatingForm()
    comment_form = CommentForm()
    
    context = {
        'restaurant': restaurant,
        'ratings': ratings,
        'comments': comments,
        'rating_form': rating_form,
        'comment_form': comment_form
    }
    return render(request, 'review/review_page.html', context)
