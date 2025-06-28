# Enhanced University Management System Models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class User(AbstractUser):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    
    ROLE_CHOICES = (
        (ADMIN, 'Administrator'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    head = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': User.TEACHER}
    )

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    credits = models.PositiveIntegerField(default=3)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': User.STUDENT})
    student_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': User.TEACHER})
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)


class Enrollment(models.Model):
    """Student course enrollment"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['student', 'course']

class Assignment(models.Model):
    """Assignment model"""
    ASSIGNMENT_TYPES = (
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('midterm', 'Mid-term Exam'),
        ('final', 'Final Exam'),
        ('project', 'Project'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPES)
    max_marks = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"

    class Meta:
        ordering = ['-due_date']

class Grade(models.Model):
    """Student grades with automatic calculation"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    graded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def percentage(self):
        return (self.marks_obtained / self.assignment.max_marks) * 100

    @property
    def letter_grade(self):
        percentage = self.percentage
        if percentage >= 90: return 'A+'
        elif percentage >= 85: return 'A'
        elif percentage >= 80: return 'A-'
        elif percentage >= 75: return 'B+'
        elif percentage >= 70: return 'B'
        elif percentage >= 65: return 'B-'
        elif percentage >= 60: return 'C+'
        elif percentage >= 55: return 'C'
        elif percentage >= 50: return 'C-'
        else: return 'F'

    class Meta:
        unique_together = ['student', 'assignment']

class Announcement(models.Model):
    """Announcements system with priority"""
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    TARGET_AUDIENCE = (
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('teachers', 'Teachers Only'),
        ('department', 'Department Specific'),
        ('course', 'Course Specific'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    target_audience = models.CharField(max_length=20, choices=TARGET_AUDIENCE, default='all')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"

    class Meta:
        ordering = ['-created_at', '-priority']

class Attendance(models.Model):
    """Attendance tracking"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    marked_by = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'course', 'date']

class Notification(models.Model):
    """User notifications"""
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

# Signal handlers for automatic profile creation
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create profile based on user type"""
    if created:
        if instance.user_type == 'teacher':
            TeacherProfile.objects.create(
                user=instance,
                employee_id=f"EMP_{instance.id:06d}",
                join_date=timezone.now().date(),
                designation="Assistant Professor"
            )
        elif instance.user_type == 'student':
            Student.objects.create(
                user=instance,
                student_id=f"STU_{instance.id:06d}",
                enrollment_date=timezone.now().date(),
                year=1,
                semester=1
            )
