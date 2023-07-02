
# Create your views here.
import os
from django.shortcuts import render
import requests


GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

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
            restaurants.append({
                "name": result["name"],
                "category": category,
                "address": result["formatted_address"],
                "latitude": result["geometry"]["location"]["lat"],
                "longitude": result["geometry"]["location"]["lng"],
                "image_url" : image_url,
                
            })
    return render(request, "restaurants/categories.html",{"restaurants": restaurants})

    

   