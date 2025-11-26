from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('connect-telegram/', views.connect_telegram_view, name='connect_telegram'),
    path('telegram-login/', views.telegram_login_callback, name='telegram_login_callback'),
    path('link-telegram/', views.link_telegram_callback, name='link_telegram_callback'),
    path('upload-documents/', views.upload_documents, name='upload_documents'),
]
