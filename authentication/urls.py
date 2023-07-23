from django.urls import path

from . import views
from knox import views as knox_views

from .views import RegisterAPI

urlpatterns = [
    path('login/', views.LoginAPI.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('register/', RegisterAPI.as_view(), name='knox_register'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logout_all'),
]
