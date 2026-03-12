from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from main.models import Note, Instruction, Assessment, FraudAlert, Notification, ActivityLog

def is_teacher(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_teacher)
def dashboard(request):
    notes = Note.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    instructions = Instruction.objects.filter(created_by=request.user).order_by('-created_at')
    alerts = FraudAlert.objects.all().order_by('-timestamp')
    students = User.objects.filter(is_staff=False)
    
    context = {
        'notes_count': notes.count(),
        'instructions_count': instructions.count(),
        'alerts_count': alerts.count(),
        'students_count': students.count(),
        'recent_notes': notes[:5],
    }
    return render(request, 'teacher/dashboard.html', context)

@login_required
@user_passes_test(is_teacher)
def fraud_alerts(request):
    alerts = FraudAlert.objects.all().order_by('-timestamp')
    return render(request, 'teacher/fraud_alerts.html', {'alerts': alerts})

@login_required
@user_passes_test(is_teacher)
def upload_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        
        if title and file:
            Note.objects.create(title=title, file=file, uploaded_by=request.user)
            messages.success(request, "Note uploaded successfully!")
        else:
            messages.error(request, "Please provide title and file.")
            
    return redirect('teacher:teacher_dashboard')

@login_required
@user_passes_test(is_teacher)
def post_instruction(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Instruction.objects.create(title=title, content=content, created_by=request.user)
            messages.success(request, "Instruction posted!")
    return redirect('teacher:teacher_dashboard')

@login_required
@user_passes_test(is_teacher)
def create_assessment(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        file = request.FILES.get('file')

        if title and description and deadline:
            Assessment.objects.create(
                title=title,
                description=description,
                deadline=deadline,
                file=file,
                created_by=request.user
            )
            messages.success(request, "Assessment created successfully!")
            return redirect('teacher:teacher_dashboard')
        else:
            messages.error(request, "Please fill all required fields.")
    
    return render(request, 'teacher/assessment_form.html')
@login_required
@user_passes_test(is_teacher)
def broadcast_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')
        
        if subject and message_body:
            students = User.objects.filter(is_staff=False)
            recipient_list = [student.email for student in students if student.email]
            
            # Send email
            # send_mail(subject, message_body, 'nexo-noreply@example.com', recipient_list)
            
            # Create a notification record
            Notification.objects.create(title=subject, message=message_body)
            messages.success(request, f"Broadcast sent to {len(recipient_list)} students!")
        else:
            messages.error(request, "Subject and Message are required.")
            
    return redirect('teacher:teacher_dashboard')

@login_required
@user_passes_test(is_teacher)
def activity_logs(request):
    logs = ActivityLog.objects.all().order_by('-timestamp')
    return render(request, 'teacher/activity_logs.html', {'logs': logs})

@login_required
@user_passes_test(is_teacher)
def broadcast_alert(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        if title and message:
            Notification.objects.create(title=title, message=message, is_alert=True)
            messages.success(request, "Immediate alert broadcasted!")
    return redirect('teacher:teacher_dashboard')

from django.shortcuts import get_object_or_404
@login_required
@user_passes_test(is_teacher)
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, uploaded_by=request.user)
        note.delete()
        messages.success(request, "Note deleted successfully.")
    except Note.DoesNotExist:
        messages.error(request, "Note not found or you don't have permission to delete it.")
    
    return redirect('teacher:teacher_dashboard')


