from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Grade, Administrator, CourseManagement
from .forms import CourseForm, EnrollmentForm, GradeForm, CourseManagementForm, UserRegistrationForm

@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    grades = Grade.objects.filter(enrollment__student=student)
    return render(request, 'mainapp/student_dashboard.html', {
        'student': student,
        'enrollments': enrollments,
        'grades': grades
    })

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    courses = Course.objects.all()
    students = Student.objects.all()
    enrollments = Enrollment.objects.all()
    grades = Grade.objects.all()
    return render(request, 'mainapp/admin_dashboard.html', {
        'courses': courses,
        'students': students,
        'enrollments': enrollments,
        'grades': grades
    })

@user_passes_test(lambda u: u.is_superuser)
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'mainapp/course_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def enroll_student(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EnrollmentForm()
    return render(request, 'mainapp/enrollment_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def assign_grade(request, enrollment_id):
    enrollment = Enrollment.objects.get(pk=enrollment_id)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.enrollment = enrollment
            grade.save()
            return redirect('admin_dashboard')
    else:
        form = GradeForm()
    return render(request, 'mainapp/grade_form.html', {'form': form, 'enrollment': enrollment})

@user_passes_test(lambda u: u.is_superuser)
def manage_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = CourseManagementForm(request.POST)
        if form.is_valid():
            management = form.save(commit=False)
            management.course = course
            management.admin = Administrator.objects.get(user=request.user)
            management.save()
            return redirect('admin_dashboard')
    else:
        form = CourseManagementForm()
    return render(request, 'mainapp/course_management_form.html', {'form': form, 'course': course})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'mainapp/register.html', {'form': form})

def homepage(request):
    return render(request, 'mainapp/homepage.html')