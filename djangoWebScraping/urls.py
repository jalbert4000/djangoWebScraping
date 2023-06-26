from django.contrib import admin
from django.urls import path, include
#from djangoWebScraping.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('inicio', inicio),
    path('',include('scraping.urls'))
]