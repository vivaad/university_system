from django.test import TestCase
from django.urls import reverse
from .models import Students, Administrators

class CoreViewsTests(TestCase):

    def setUp(self):
        self.admin = Administrators.objects.create(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password_hash='hashed_password'
        )
        self.student = Students.objects.create(
            first_name='Student',
            last_name='User',
            email='student@example.com',
            password_hash='hashed_password',
            date_of_birth='2000-01-01',
            enrollment_year=2023
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_admin_login(self):
        response = self.client.post(reverse('login'), {
            'email': 'admin@example.com',
            'password': 'hashed_password'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_student_login(self):
        response = self.client.post(reverse('login'), {
            'email': 'student@example.com',
            'password': 'hashed_password'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_admin_registration(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'Admin',
            'email': 'newadmin@example.com',
            'password': 'new_hashed_password'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(Administrators.objects.filter(email='newadmin@example.com').exists())

    def test_student_registration(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'Student',
            'email': 'newstudent@example.com',
            'password': 'new_hashed_password',
            'date_of_birth': '2001-01-01',
            'enrollment_year': 2023
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(Students.objects.filter(email='newstudent@example.com').exists())

    def test_logout(self):
        self.client.login(email='admin@example.com', password='hashed_password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/logout.html')