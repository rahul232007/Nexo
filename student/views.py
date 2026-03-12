from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from main.models import Note, Instruction, Assessment, Submission, Notification, ActivityLog, FraudAlert
import json

def log_activity(user, action, details=None):
    ActivityLog.objects.create(user=user, action=action, details=details)

@login_required
def dashboard(request):
    notes = Note.objects.all().order_by('-uploaded_at')
    instructions = Instruction.objects.all().order_by('-created_at')
    pending_assessments = Assessment.objects.filter(deadline__gte=timezone.now())
    
    notifications = Notification.objects.filter(recipient__isnull=True).order_by('-created_at')[:5]
    
    # Log the visit
    log_activity(request.user, "Dashboard Visit", "Student accessed the dashboard.")

    context = {
        'notes': notes,
        'instructions': instructions,
        'notes_count': notes.count(),
        'instructions_count': instructions.count(),
        'assessments_count': pending_assessments.count(),
        'notifications': notifications,
    }
    return render(request, 'student/dashboard.html', context)

@login_required
def assessment_list(request):
    assessments = Assessment.objects.filter(deadline__gte=timezone.now()).order_by('deadline')
    return render(request, 'student/assessment_list.html', {'assessments': assessments})

@login_required
def submit_assessment(request, assessment_id):
    if request.method == 'POST':
        assessment = get_object_or_404(Assessment, id=assessment_id)
        file = request.FILES.get('submission_file')
        
        if file:
            Submission.objects.create(
                student=request.user,
                assessment=assessment,
                file=file
            )
            messages.success(request, f"Submitted work for {assessment.title}!")
        else:
            messages.error(request, "Please attach a file.")
            
    return redirect('student:assessment_list')

@csrf_exempt
@login_required
def track_fraud(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            alert_type = data.get('alert_type')
            details = data.get('details')
            
            FraudAlert.objects.create(
                student=request.user,
                alert_type=alert_type,
                details=details
            )
            log_activity(request.user, "Fraudulent Action", f"{alert_type}: {details}")
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)
