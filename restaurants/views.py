
# Create your views here.
import os
from django.shortcuts import render, get_object_or_404, redirect, reverse
import requests
from review.models import Restaurant, Review
from users.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import NoReverseMatch
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

def get_place_details(place_id):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "website,photos",
        "key": GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(details_url, params=params)
    details_data = response.json()
    return details_data.get("result", {})


def restaurants(request, category):
    if category == "asian":
        
        url = (
            f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=Asian%20restaurants%20in%20Dublin&key={GOOGLE_PLACES_API_KEY}"
        )
            
    elif category == "european":
        url = (
            f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=European%20restaurants%20in%20Dublin&key={GOOGLE_PLACES_API_KEY}"
        )
    elif category == "african":
        url = (
            f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=African%20restaurants%20in%20Dublin&key={GOOGLE_PLACES_API_KEY}"
        )
    elif category == "irish":
        url = (
            f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=Irish%20restaurants%20in%20Dublin&key={GOOGLE_PLACES_API_KEY}"
        )
    elif category == "american":
        url = (
            f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=American%20restaurants%20in%20Dublin&key={GOOGLE_PLACES_API_KEY}"
        )
    elif category == "all":
        url = (
            f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=All%20restaurants%20in%20Dublin&key={GOOGLE_PLACES_API_KEY}"
        )
    else:
        pass
    user = request.user
    restaurants = []
    response = requests.get(url)
    restaurant_data = response.json()
    results = restaurant_data.get("results", [])
    # print(results)    
    paginator = Paginator(results, 8)  
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    
    for result in page_object:
            
            place_id = result.get("place_id")
            if place_id:
                details_data = get_place_details(place_id)
                website_url = details_data.get("website", "")
                photos = details_data.get("photos", "")
                image_urls = []
                if photos:
                    for photo in photos:
                        photo_reference = photo.get('photo_reference')
                        if photo_reference:
                            image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"
                            image_urls.append(image_url)
                else:
                    image_urls.append("https://res.cloudinary.com/dif9bjzee/image/upload/v1688163762/backgroud_hwsqzo.webp")
            
            else:
                website_url = ""

            try:
                restaurant_details = Restaurant.objects.get(RestaurantId=place_id)
            except Restaurant.DoesNotExist:
                restaurant_details = Restaurant(
                    name = result["name"],
                    website = website_url,
                    category = category,
                    address = result["formatted_address"],
                    RestaurantId = place_id,
                )            
                print(restaurant_details)
                restaurant_details.save()
            
            # user_review = Review.objects.filter(restaurant=restaurant_details, user=user)
            # profile = Profile.objects.get(user=user)
            # # print(user_review)
            # if profile.pinned_restaurants.filter(RestaurantId=place_id).exists():
            #     pinned = True
            # else:
            #     pinned = False
                
            # if user_review.exists():
            #     user_reviewed = True
            # else:
            #     user_reviewed = False
            pinned = False
            user_reviewed = False  # Initialize the user_reviewed variable to False
            if request.user.is_authenticated:
                  # If the user is signed in, check if they have reviewed the restaurant
                user_review = Review.objects.filter(restaurant=restaurant_details, user=user)
                profile = Profile.objects.get(user=user)
                if user_review.exists():
                    user_reviewed = True
                if profile.pinned_restaurants.filter(RestaurantId=place_id).exists():
                    pinned = True
            
            restaurants.append({
                "name": result["name"],
                "category": category,
                "address": result["formatted_address"],
                "latitude": result["geometry"]["location"]["lat"],
                "longitude": result["geometry"]["location"]["lng"],
                "image_urls" : image_urls,
                "user_reviewed": user_reviewed,
                "pinned":pinned,
                "website_url": website_url,
                "place_id": place_id,
                
            })

            
    # print(restaurants)
    return render(request, 'restaurants/categories.html', {
        "restaurants":restaurants,
        "page_object": page_object,
        
        })

@login_required
def to_visit(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, RestaurantId=restaurant_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if restaurant in profile.pinned_restaurants.all():
        profile.pinned_restaurants.remove(restaurant)
        messages.success(
            request,
            f"{user.username} you have removed {restaurant} from your profile",
        )
    else:
        profile.pinned_restaurants.add(restaurant)
        messages.success(
            request,
            f"{user.username} you have added {restaurant} to your profile",
        )

    # category_url = reverse('{}'.format(restaurant.category))
    # return redirect(category_url)
    try:
        category_url = reverse(restaurant.category)
    except NoReverseMatch:
        return redirect(request.META.get('HTTP_REFERER'))
    # category_url = reverse('{}'.format(restaurant.category))
    return redirect(category_url)
    

def remove_pin(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, RestaurantId=restaurant_id)
    
    user = request.user
    profile = Profile.objects.get(user=user)

    if restaurant in profile.pinned_restaurants.all():
        profile.pinned_restaurants.remove(restaurant)
        messages.success(
            request,
            f"{user.username} you have removed {restaurant} from your profile",
        )

    return redirect("profile", username=user.username)


def profile_reviews(request, restaurant_id):
    
    #restaurant = Restaurant.objects.get(RestaurantId=restaurant_id)
    restaurant = get_object_or_404(Restaurant, RestaurantId=restaurant_id)

    user = request.user
    # profile = Profile.objects.get(user=user)
    profile = get_object_or_404(Profile, user=user)
    review = get_object_or_404(Review, user=user,restaurant=restaurant)
    if review:
        if restaurant in profile.reviewed.all():
            return redirect(reverse("edit_review", args=[restaurant_id, review.id]))
