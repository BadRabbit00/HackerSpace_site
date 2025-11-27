from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('create/', views.create_news, name='create_news'),
]
