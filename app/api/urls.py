from django.contrib import admin
from django.urls import path, include

from .views import reply, dataParsing, get_place_based_hashtag

urlpatterns = [
    path('reply', reply),
    path('parsing', dataParsing),
    path('hashtag', get_place_based_hashtag),
]