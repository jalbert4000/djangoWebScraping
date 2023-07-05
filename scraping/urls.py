from django.urls import path
from scraping.views import webscraping
from scraping.views import webscrapingv2
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',webscraping),
    path('/test',webscrapingv2)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)