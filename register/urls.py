
from django.urls import path

from register import views

app_name = "register"

urlpatterns = [
    # path('auth/', views.index , name='register'),
    path('registration/', views.reg, name='reg')
    
]