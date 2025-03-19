# filepath: my_django_project/myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField()

    def __str__(self):
        return self.course_name

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment.student} - {self.enrollment.course}: {self.grade}"

class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class CourseManagement(models.Model):
    management_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=255)
    action_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin} managed {self.course}"