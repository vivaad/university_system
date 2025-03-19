# Student Management System

This is a Django-based web application for managing students, courses, enrollments, and grades. The application provides separate dashboards for administrators and students, allowing for efficient management and access to relevant information.

## Features

- User authentication for both administrators and students.
- Admin dashboard for managing students and courses.
- Student dashboard for viewing enrolled courses and grades.
- Registration functionality for new administrators and students.
- Logout functionality for secure session management.

## Project Structure

```
student_management_system/
├── manage.py
├── student_management_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── core/
│           ├── home.html
│           ├── login.html
│           ├── admin_dashboard.html
│           ├── student_dashboard.html
│           ├── register.html
│           └── logout.html
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd student_management_system
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Use the homepage to log in as an admin or student.
- Admins can manage students and courses from the admin dashboard.
- Students can view their enrolled courses and grades from the student dashboard.
- New users can register from the registration page.

## License

This project is licensed under the MIT License.