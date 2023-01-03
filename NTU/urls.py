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
    path('', include("news.urls"), name="new"),
    path('', index, name='index')
]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)