from django.contrib import admin
from .models import Restaurant, Review

admin.site.register(Restaurant)
admin.site.register(Review)
# admin.site.register(Comment)