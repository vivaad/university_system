# filepath: /home/vivek/bakchodi/New DBS/better/myapp/forms.py
from django import forms
from .models import Course, Enrollment, Grade, CourseManagement, User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'credits']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']

class CourseManagementForm(forms.ModelForm):
    class Meta:
        model = CourseManagement
        fields = ['action_taken']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data