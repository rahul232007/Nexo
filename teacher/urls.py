from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.dashboard, name='teacher_dashboard'),
    path('upload_note/', views.upload_note, name='upload_note'),
    path('post_instruction/', views.post_instruction, name='post_instruction'),
    path('create_assessment/', views.create_assessment, name='create_assessment'),
    path('broadcast_email/', views.broadcast_email, name='broadcast_email'),
    path('broadcast_alert/', views.broadcast_alert, name='broadcast_alert'),
    path('activity_logs/', views.activity_logs, name='activity_logs'),
    path('fraud_alerts/', views.fraud_alerts, name='fraud_alerts'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
]
