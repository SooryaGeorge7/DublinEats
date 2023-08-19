
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
    profile = get_object_or_404(Profile, user= user)
    
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
            profile.reviewed.add(restaurant)
            # restaurant_comment.save()
            messages.success(
                request, f"{user.username} you have reviewed {restaurant}"
            )
            return redirect(reverse("allreviews", kwargs={'restaurant_id': restaurant_id}))
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

@login_required()
def allreviews(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, RestaurantId=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant)
    context = {
        "reviews": reviews,
        "restaurant":restaurant,
    }

    return render(request, "review/allreviews.html", context)

@login_required()
def edit_review(request, restaurant_id, review_id):
    user = request.user
    # restaurant = Restaurant.objects.get(RestaurantId=restaurant_id)
    restaurant = get_object_or_404(Restaurant, RestaurantId=restaurant_id)
    user_review = Review.objects.filter(restaurant=restaurant, user=user)
    review = get_object_or_404(Review, id=review_id)
    
    
    if user_review.exists() or user.is_superuser:
        user_reviewed = True
    else:
        user_reviewed = False
    if review.user != user and not user.is_superuser:
        messages.error(request, "You are not authorized to edit this review.")
        return redirect(reverse("allreviews" , kwargs={'restaurant_id': restaurant_id}))

    if request.method == "POST":
        rating_form = RatingForm(request.POST, instance=review)
        if rating_form.is_valid():
            restaurant_rating = rating_form.save(commit=False)
            restaurant_rating.save()
            messages.success(
                request, f"{user.username} your review has been updated"
            )

            return redirect(reverse("allreviews", kwargs={'restaurant_id': restaurant_id}))
        else:
            messages.success(
                request,
                "something went wrong.",
            )
    else:
        rating_form = RatingForm(instance=review)

    context = {
        "rating_form": rating_form,
        "review":review,
        "user_review": user_review,
        "restaurant": restaurant,
        "user_reviewed": user_reviewed,
    }

    return render(request, "review/review_page.html", context)

@login_required()
def delete_review(request, restaurant_id, review_id):
    restaurant = get_object_or_404(Restaurant, RestaurantId=restaurant_id)
    review = get_object_or_404(Review, id=review_id)
    user = request.user
    username = user.username
    if not user.is_superuser and review.user != user:
        messages.error(
            request, "You are not authorized to delete this review."
        )
        return redirect(reverse(f'{restaurant.category}'))

    profile = Profile.objects.get(user=review.user)
    if review.restaurant in profile.reviewed.all():
        profile.reviewed.remove(review.restaurant)

    review.delete()
    if user.is_superuser:
        messages.success(request, f"{review.user}'s review for {restaurant} has been deleted ")
    else:
        messages.success(request, f"Your review for {restaurant} has been deleted {user.username} ")
    return redirect(reverse(f'{restaurant.category}'))
    # return redirect("profile")