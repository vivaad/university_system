from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create_course/', views.create_course, name='create_course'),
    path('enroll_student/', views.enroll_student, name='enroll_student'),
    path('assign_grade/<int:enrollment_id>/', views.assign_grade, name='assign_grade'),
    path('manage_course/<int:course_id>/', views.manage_course, name='manage_course'),
    path('register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]
