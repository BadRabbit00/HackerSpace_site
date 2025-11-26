from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='account_dashboard'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('payment/initiate/<int:plan_id>/', views.initiate_payment, name='initiate_payment'),
]
