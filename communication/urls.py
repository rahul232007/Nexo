from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    path('', views.global_chat, name='global_chat'),
    path('send/<int:room_id>/', views.send_message, name='send_message'),
    path('messages/<int:room_id>/', views.get_messages, name='get_messages'),
]
