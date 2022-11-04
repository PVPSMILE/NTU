
from django.urls import path

from register import views

app_name = "register"

urlpatterns = [
    # path('auth/', views.index , name='register'),
    path('registration/', views.reg, name='reg'),
    path('code/', views.send_code, name='code'),
    path('auth/', views.auth, name='auth'),
    path('sign_out/', views.sing_out, name='sign_out'),
    path('settings/', views.setup_data, name='update'),
    
]