
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

    restaurants = []
    response = requests.get(url)
    restaurant_data = response.json()
    results = restaurant_data.get("results", [])
    print("RESPONSE: ", response)
    print("RESTAURANT_DATA:", restaurant_data)
    paginator = Paginator(results, 10)  # Show 10 restaurants per page

    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    for result in page_object:
            
            place_id = result.get("place_id")
            if place_id:
                details_data = get_place_details(place_id)
                website_url = details_data.get("website", "")
                photos = details_data.get("photos", "")
                image_urls = []
                for photo in photos:
                    photo_reference = photo.get('photo_reference')
                    if photo_reference:
                        image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"
                        image_urls.append(image_url)
                    else:
                        image_urls.append("no image")
            
            else:
                website_url = ""

            restaurants.append({
                "name": result["name"],
                "category": category,
                "address": result["formatted_address"],
                "latitude": result["geometry"]["location"]["lat"],
                "longitude": result["geometry"]["location"]["lng"],
                "image_urls" : image_urls,
                "website_url": website_url,
                "place_id": place_id,
                
            })

            try:
                restaurant_details = Restaurant.objects.get(RestaurantId=place_id)
            except Restaurant.DoesNotExist:
                restaurant_details = Restaurant(
                    name = result["name"],
                    website = website_url,
                    address = result["formatted_address"],
                    RestaurantId = place_id,
                )            
                restaurant_details.save()
    return render(request, 'restaurants/categories.html', {
        "restaurants":restaurants,
        "page_object": page_object,
        })
                
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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

    return redirect("profile")

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
