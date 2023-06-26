from django.urls import path
from scraping.views import webscraping
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',webscraping)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)