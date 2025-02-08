from django.urls import path
from . import views

app_name = 'student_management'

urlpatterns = [
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/courses/', views.manage_courses, name='manage_courses'),
    path('admin/enroll/', views.enroll_student, name='enroll_student'),
    path('admin/grades/', views.assign_grade, name='assign_grade'),
]
