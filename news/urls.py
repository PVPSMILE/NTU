
from django.urls import path

from news import views

app_name = "news"
urlpatterns = [
    path('news/', views.index , name='new')
]