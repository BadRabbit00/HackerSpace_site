from django.urls import path
from . import views

urlpatterns = [
    path('take/<int:item_id>/', views.take_item, name='take_item'),
]
