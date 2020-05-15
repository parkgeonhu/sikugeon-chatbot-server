from django.contrib import admin
from django.urls import path, include, re_path

from .views import reply, dataParsing, get_place_based_hashtag, ResultView

urlpatterns = [
    re_path(r'^test/((?P<shortcode>[\w-]+)?)$',ResultView.as_view(), name='result'),
    path('reply', reply),
    path('parsing', dataParsing),
    path('hashtag', get_place_based_hashtag),
]