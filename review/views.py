from django.shortcuts import render

# Create your views here.
import os

import requests


API_KEY = os.environ.get("API_KEY")


def review(request,):
    
    return render(request, "review/review.html",)
