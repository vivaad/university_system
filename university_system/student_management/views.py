from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Registration, Grade
from .forms import EnrollForm, GradeForm, CourseForm
from .models import DataPoint
import json
# Student Dashboard


@login_required
def student_dashboard(request):
    # if request.user.profile.role != 'student':
    #     return redirect('student_management:admin_dashboard')  # add the namespace

    registrations = Registration.objects.filter(student=request.user)
    grades = Grade.objects.filter(student=request.user)

    labels = [grade.course.name for grade in grades]
    values = [grade.value for grade in grades]

    context = {
        'registrations': registrations,
        'grades': grades,
        'labels': json.dumps(labels),
        'values': json.dumps(values),
    }
    return render(request, 'student_management/student_dashboard.html', context)

# Admin Dashboard


@login_required
# @user_passes_test(lambda u: u.profile.role == 'admin')
def admin_dashboard(request):
    courses = Course.objects.count()
    students = Registration.objects.values('student').distinct().count()
    return render(request, 'student_management/admin_dashboard.html', {'courses': courses, 'students': students})


# Manage Courses


@login_required
# @user_passes_test(lambda u: u.profile.role == 'admin')
def manage_courses(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm()
    return render(request, 'student_management/manage_courses.html', {'courses': courses, 'form': form})

# Enroll Students


@login_required
# @user_passes_test(lambda u: u.profile.role == 'admin')
def enroll_student(request):
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll_student')
    else:
        form = EnrollForm()
    return render(request, 'student_management/enroll_student.html', {'form': form})

# Assign Grades


@login_required
# @user_passes_test(lambda u: u.profile.role == 'admin')
def assign_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assign_grade')
    else:
        form = GradeForm()
    return render(request, 'student_management/assign_grade.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.profile.role == 'admin')
def chart_view(request):
    data = DataPoint.objects.all()
    labels = [item.timestamp.strftime("%Y-%m-%d") for item in data]
    values = [item.value for item in data]

    context = {
        'labels': json.dumps(labels),
        'values': json.dumps(values),
    }
    return render(request, 'student_management/chart.html', context)

@login_required
def update_data(request):
    data = DataPoint.objects.all()
    html = render_to_string('student_management/data_partial.html', {'data': data})
    return HttpResponse(html)