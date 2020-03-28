from django.contrib import admin
from django.urls import path, include

from .views import reply, dataParsing

urlpatterns = [
    path('reply/', reply),
    path('parsing/', dataParsing),
]