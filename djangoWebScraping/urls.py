from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from djangoWebScraping.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('inicio', inicio),
    path('',include('scraping.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)