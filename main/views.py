from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful 🎉")
            if user.is_staff or user.is_superuser:
                return redirect("teacher:teacher_dashboard")
            else:
                return redirect("student:student_dashboard")

        else:
            messages.error(request, "Invalid username or password 😬")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully 👋")
    return redirect("main:login")




def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        role = request.POST.get('role')

        if password != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            
            if role == 'teacher':
                user.is_staff = True
                user.save()
                messages.success(request, "Teacher account created successfully! Please login.")
            else:
                messages.success(request, "Student account created successfully! Please login.")
            
            return redirect('main:login')

    return render(request, 'register.html')






