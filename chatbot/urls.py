from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('api/', views.chat_api, name='chat_api'),
    path('health/', views.chat_health, name='chat_health'),
    path('clear/', views.clear_chat_session, name='clear_chat_session'),

]
