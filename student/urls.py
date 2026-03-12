from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('assessments/', views.assessment_list, name='assessment_list'),
    path('submit/<int:assessment_id>/', views.submit_assessment, name='submit_assessment'),
    path('track_fraud/', views.track_fraud, name='track_fraud'),
]
