
# Create your views here.
import os
from django.shortcuts import render
import requests


GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

