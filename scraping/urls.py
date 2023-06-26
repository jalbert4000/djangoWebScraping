from django.urls import path
from scraping.views import webscraping
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',webscraping)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)