from django import forms
from .models import Course, Registration, Grade, User


class EnrollForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='student'))
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    def save(self):
        student = self.cleaned_data['student']
        course = self.cleaned_data['course']
        Registration.objects.get_or_create(student=student, course=course)


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'grade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(
            profile__role='student')
        self.fields['course'].queryset = Course.objects.all()


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'name', 'description']
