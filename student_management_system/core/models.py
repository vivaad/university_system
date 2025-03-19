from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Student(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_year = models.IntegerField(null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='student_set')
    user_permissions = models.ManyToManyField(Permission, related_name='student_set')

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField()

    def __str__(self):
        return self.course_name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    graded_at = models.DateTimeField(auto_now_add=True)

class Administrator(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='administrator_set')
    user_permissions = models.ManyToManyField(Permission, related_name='administrator_set')

class CourseManagement(models.Model):
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    action_taken = models.CharField(max_length=255)
    action_date = models.DateTimeField(auto_now_add=True)