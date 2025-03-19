from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student, Administrator
from .forms import StudentRegistrationForm, AdminRegistrationForm

def home(request):
    return render(request, 'core/home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'core/login.html')

@login_required
def dashboard(request):
    if request.user.is_staff:
        return render(request, 'core/admin_dashboard.html')
    else:
        return render(request, 'core/student_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

@login_required
def student_dashboard(request):
    return render(request, 'core/student_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    student_form = StudentRegistrationForm()
    admin_form = AdminRegistrationForm()
    
    if request.method == 'POST':
        if 'is_admin' in request.POST:
            form = AdminRegistrationForm(request.POST)
        else:
            form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'core/register.html', {'student_form': student_form, 'admin_form': admin_form})