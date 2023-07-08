
# Create your views here.
import os
from django.shortcuts import render
import requests
from review.models import Restaurant


GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

def get_place_details(place_id):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "website",
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

    for result in results:
            photo_reference = result.get('photos', [])[0].get('photo_reference')
            if photo_reference:
                image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"
            else:
                image_url = "no image"
            place_id = result.get("place_id")
            if place_id:
                details_data = get_place_details(place_id)
                website_url = details_data.get("website", "")
            
            else:
                website_url = ""

            restaurants.append({
                "name": result["name"],
                "category": category,
                "address": result["formatted_address"],
                "latitude": result["geometry"]["location"]["lat"],
                "longitude": result["geometry"]["location"]["lng"],
                "image_url" : image_url,
                "website_url": website_url,
                "place_id": place_id,
            })
            
    return render(request, "restaurants/categories.html",{"restaurants": restaurants})


    

   