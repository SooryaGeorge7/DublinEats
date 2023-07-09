
from .forms import RatingForm
from .models import Restaurant, Review
from django.contrib.auth.models import User
from users.models import Profile
import os
from django.shortcuts import render, get_object_or_404, redirect, reverse
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required()
def review(request, restaurant_id):
    restaurant = Restaurant.objects.get(RestaurantId= restaurant_id)
    ratings = Review.objects.filter(restaurant=restaurant)
    # comments = Comment.objects.filter(restaurant=restaurant)
    user = request.user
    # # rating_form = RatingForm()
    # # comment_form = CommentForm()
    
            
    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        # comment_form = CommentForm(request.POST)
        if rating_form.is_valid() :
            restaurant_rating = rating_form.save(commit=False)
            # restaurant_comment = comment_form.save(commit=False)
            restaurant_rating.restaurant = restaurant
            # restaurant_comment.restaurant = restaurant
            restaurant_rating.user = user
            # restaurant_comment.user = user
            restaurant_rating.save()
            # restaurant_comment.save()
            messages.success(
                request, f"{user.username} you have reviewed {restaurant}"
            )
            return redirect("dublineats-home")
        else:
            # error_message = rating_form.errors.as_text()
            # messages.error(request, f"Error: {error_message}")
            messages.error(
                request,
                "something went wrong.",
            )
    else:
        rating_form = RatingForm()
        # comment_form = CommentForm()
    
    context = {
        'restaurant': restaurant,
        'ratings': ratings,
        # 'comments': comments,
        'rating_form': rating_form,
        # 'comment_form': comment_form,
    }
    return render(request, 'review/review_page.html', context)
