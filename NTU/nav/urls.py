
from django.urls import path

from nav import views

app_name="nav"

urlpatterns = [
    # path('register/', views.register , name='register'),
    path('campus/<int:pk>/', views.nav, name='campus'),
    path('navigation/', views.nav, name="navigation")
]