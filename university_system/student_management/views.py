from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Registration, Grade
from .forms import EnrollForm, GradeForm, CourseForm

# Student Dashboard


@login_required
def student_dashboard(request):
    if request.user.profile.role != 'student':
        return redirect('admin_dashboard')
    registrations = Registration.objects.filter(student=request.user)
    grades = Grade.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {'registrations': registrations, 'grades': grades})

# Admin Dashboard


@login_required
@user_passes_test(lambda u: u.profile.role == 'admin')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Manage Courses


@login_required
@user_passes_test(lambda u: u.profile.role == 'admin')
def manage_courses(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm()
    return render(request, 'manage_courses.html', {'courses': courses, 'form': form})

# Enroll Students


@login_required
@user_passes_test(lambda u: u.profile.role == 'admin')
def enroll_student(request):
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll_student')
    else:
        form = EnrollForm()
    return render(request, 'enroll_student.html', {'form': form})

# Assign Grades


@login_required
@user_passes_test(lambda u: u.profile.role == 'admin')
def assign_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assign_grade')
    else:
        form = GradeForm()
    return render(request, 'assign_grade.html', {'form': form})
