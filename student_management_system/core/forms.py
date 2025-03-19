from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Administrator

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'enrollment_year', 'password1', 'password2']

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']