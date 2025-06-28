from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import *
from .forms import *

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        user = authenticate(username=username, password=password)
        if user and user.user_type == user_type:
            login(request, user)
            return redirect(f'{user_type}_dashboard')
        else:
            messages.error(request, 'Invalid credentials or user type')
    
    return render(request, 'auth/login.html')

def admin_login(request):
    return render(request, 'auth/admin_login.html')

def teacher_login(request):
    return render(request, 'auth/teacher_login.html')

def student_login(request):
    return render(request, 'auth/student_login.html')

# Role-based test functions
def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def is_teacher(user):
    return user.is_authenticated and user.user_type == 'teacher'

def is_student(user):
    return user.is_authenticated and user.user_type == 'student'

# Dashboard Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    stats = {
        'total_students': User.objects.filter(user_type='student').count(),
        'total_teachers': User.objects.filter(user_type='teacher').count(),
        'total_courses': Course.objects.count(),
        'total_departments': Department.objects.count(),
        'recent_enrollments': CourseEnrollment.objects.select_related('student__user', 'course').order_by('-enrolled_date')[:5],
        'recent_announcements': Announcement.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin/dashboard.html', stats)

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher_profile = get_object_or_404(TeacherProfile, user=request.user)
    
    enrollments = CourseEnrollment.objects.filter(teacher=teacher_profile).select_related('course', 'student__user')
    courses = Course.objects.filter(courseenrollment__teacher=teacher_profile).distinct()
    
    stats = {
        'total_courses': courses.count(),
        'total_students': enrollments.count(),
        'recent_grades': Grade.objects.filter(assignment__course__in=courses).order_by('-graded_at')[:10],
        'courses': courses,
        'teacher_profile': teacher_profile,
    }
    return render(request, 'teacher/dashboard.html', stats)

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    
    enrollments = CourseEnrollment.objects.filter(student=student_profile).select_related('course', 'teacher__user')
    grades = Grade.objects.filter(student=student_profile).select_related('assignment__course')
    
    # Calculate GPA
    if grades.exists():
        avg_percentage = grades.aggregate(avg=Avg('marks_obtained'))['avg'] or 0
        gpa = (avg_percentage / 100) * 4.0
        student_profile.gpa = round(gpa, 2)
        student_profile.save()
    
    stats = {
        'enrollments': enrollments,
        'grades': grades.order_by('-graded_at'),
        'gpa': student_profile.gpa,
        'student_profile': student_profile,
        'recent_announcements': Announcement.objects.filter(
            Q(target_audience='all') | Q(target_audience='students')
        ).order_by('-created_at')[:5],
    }
    return render(request, 'student/dashboard.html', stats)

# Grade Management
@login_required
@user_passes_test(is_teacher)
def grade_management(request):
    teacher_profile = get_object_or_404(TeacherProfile, user=request.user)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        assignment_id = request.POST.get('assignment_id')
        marks_obtained = request.POST.get('marks_obtained')
        feedback = request.POST.get('feedback')
        
        student = get_object_or_404(StudentProfile, student_id=student_id)
        assignment = get_object_or_404(Assignment, id=assignment_id)
        
        Grade.objects.update_or_create(
            student=student,
            assignment=assignment,
            defaults={
                'marks_obtained': marks_obtained,
                'feedback': feedback,
                'graded_by': teacher_profile
            }
        )
        messages.success(request, 'Grade updated successfully!')
        return redirect('grade_management')
    
    assignments = Assignment.objects.filter(teacher=teacher_profile, is_active=True)
    enrollments = CourseEnrollment.objects.filter(teacher=teacher_profile).select_related('student__user', 'course')
    
    return render(request, 'teacher/grade_management.html', {
        'assignments': assignments,
        'enrollments': enrollments,
    })

# Course Enrollment
@login_required
@user_passes_test(is_student)
def course_enrollment(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        
        if not CourseEnrollment.objects.filter(student=student_profile, course=course).exists():
            teacher = TeacherProfile.objects.filter(department=course.department).first()
            if teacher:
                CourseEnrollment.objects.create(
                    student=student_profile,
                    course=course,
                    teacher=teacher
                )
                messages.success(request, f'Successfully enrolled in {course.name}!')
            else:
                messages.error(request, 'No teacher available for this course.')
        else:
            messages.warning(request, 'Already enrolled in this course.')
        
        return redirect('course_enrollment')
    
    available_courses = Course.objects.filter(
        department=student_profile.department,
        semester=student_profile.semester,
        is_active=True
    ).exclude(
        courseenrollment__student=student_profile
    )
    
    enrolled_courses = CourseEnrollment.objects.filter(
        student=student_profile,
        is_active=True
    ).select_related('course', 'teacher__user')
    
    return render(request, 'student/course_enrollment.html', {
        'available_courses': available_courses,
        'enrolled_courses': enrolled_courses,
    })

# Announcements
@login_required
def announcements(request):
    if request.user.user_type == 'student':
        announcements = Announcement.objects.filter(
            Q(target_audience='all') | Q(target_audience='students'),
            is_active=True
        ).order_by('-created_at')
    elif request.user.user_type == 'teacher':
        announcements = Announcement.objects.filter(
            Q(target_audience='all') | Q(target_audience='teachers'),
            is_active=True
        ).order_by('-created_at')
    else:
        announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')
    
    return render(request, 'announcements.html', {'announcements': announcements})

@login_required
@user_passes_test(lambda u: u.user_type in ['admin', 'teacher'])
def create_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        priority = request.POST.get('priority')
        target_audience = request.POST.get('target_audience')
        
        Announcement.objects.create(
            title=title,
            content=content,
            author=request.user,
            priority=priority,
            target_audience=target_audience
        )
        messages.success(request, 'Announcement created successfully!')
        return redirect('announcements')
    
    return render(request, 'create_announcement.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
