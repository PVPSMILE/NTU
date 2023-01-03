
from django.urls import path

from news import views

app_name = "news"
urlpatterns = [
    path('news/detail/<int:primary_key>/',views.detail,name="detail"),
    path('requests/',views.admin_request_page,name="request"),
    path('requests/detail/article/<int:primary_key>/',views.admin_request_detail_article_page,name="request_detail"),
    path('requests/detail/account/<int:primary_key>/',views.admin_request_detail_account_page,name="request_detail_account"),
    path('articles/list/<int:pk>/',views.articls_page,name="list_articls"),
    path('article/detail/<int:pk>/',views.detail_article_page,name="detail_article"),
    path('article/create/',views.detail_create_article_page,name="create_article"),
    path('article/all/', views.all_article_page,name="all_news"),
    path('article/all/detail/<int:pk>/', views.all_article_detail_page,name="all_detail_news")
]