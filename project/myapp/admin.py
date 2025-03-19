# filepath: my_django_project/myapp/admin.py
from django.contrib import admin
from .models import Student, Course, Enrollment, Grade, Administrator, CourseManagement

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Grade)
admin.site.register(Administrator)
admin.site.register(CourseManagement)