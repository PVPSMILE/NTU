
from django.urls import path

from register import views

app_name = "register"

urlpatterns = [
    # path('auth/', views.index , name='register'),
    path('registration/', views.reg, name='reg'),
    path('login/', views.login, name='login'),
 

    path('code/', views.send_code, name='codeg'),

    # path('sign_out/', views.sing_out, name='sign_out'),
    # path('settings/', views.setup_data, name='update'),

    
]