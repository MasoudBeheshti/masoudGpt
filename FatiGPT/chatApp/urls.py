from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name='chatApp'


urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('accounts/login/',auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('delete-massages/', views.delete_massages, name='delete_massages'),
]