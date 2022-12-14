from django.conf import settings
from django.conf.urls.static import static

from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from news.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("register.urls"), name="reg"),
    path('', include("nav.urls"), name="nav"),
    path('', index, name='index')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

