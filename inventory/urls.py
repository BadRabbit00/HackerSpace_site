from django.urls import path
from . import views

urlpatterns = [
    path('', views.hardware_list, name='hardware_list'),
    path('take/<int:item_id>/', views.take_item, name='take_item'),
    path('manage/<int:item_id>/', views.manage_my_item, name='manage_my_item'),
    path('my-loans/', views.my_loans, name='my_loans'),
]
