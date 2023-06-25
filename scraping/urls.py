from django.urls import path
from scraping.views import webscraping

urlpatterns = [
    path('',webscraping)
]