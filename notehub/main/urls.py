from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_int/', views.register_int, name='register-int'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('feed/', views.feed, name='feed'),
]