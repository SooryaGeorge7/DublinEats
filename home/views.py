from django.shortcuts import render

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
# Create your views here.
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

def get_details(place_id):
    detail_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "website,photos",
        "key": GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(detail_url, params=params)
    detail_data = response.json()
    return detail_data.get("result", {})


def searchresults(request):
    
    query = request.GET.get("query")

    url = ( 
        f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&type=restaurant&location=53.350140,-6.266155&key={GOOGLE_PLACES_API_KEY}"
    )
    user = request.user
    restaurant_results = []
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
                detail_data = get_details(place_id)
                website_url = detail_data.get("website", "")
                photos = detail_data.get("photos", "")
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
                    address = result["formatted_address"],
                    RestaurantId = place_id,
                )            
                print(restaurant_details)
                restaurant_details.save()
            
            # user_review = Review.objects.filter(restaurant=restaurant_details, user=user)
            
            # if user_review.exists():
            #     user_reviewed = True
            # else:
            #     user_reviewed = False
            
            user_reviewed = False  # Initialize the user_reviewed variable to False
            if request.user.is_authenticated:
                  # If the user is signed in, check if they have reviewed the restaurant
                user_review = Review.objects.filter(restaurant=restaurant_details, user=user)
                if user_review.exists():
                    user_reviewed = True

            restaurant_results.append({
                "name": result["name"],
                "address": result["formatted_address"],
                "latitude": result["geometry"]["location"]["lat"],
                "longitude": result["geometry"]["location"]["lng"],
                "image_urls" : image_urls,
                "user_reviewed" : user_reviewed,
                "website_url": website_url,
                "place_id": place_id,
                
            })

            
    return render(request, 'home/results.html', {
        "restaurant_results":restaurant_results,
        "page_object": page_object,
        
        })


def home(request):
    return render(request, 'home/index.html')
