from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('signin/', views.signin, name="signin"),
]
