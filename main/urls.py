from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),       # home page
    path('login/', views.login_view, name='login'),  # login page
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
]
