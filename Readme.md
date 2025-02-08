# University Management System

A Django-based university management system for handling student records, course management, and academic operations.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12.0 or higher
- pip (Python package manager)

## Installation

1. Clone the repository
```bash
git clone https://github.com/vivek0824/university_system.git
cd university_system
```

2. Create a virtual environment and activate it
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages
```bash
pip install -r requirements.txt
```

## Database Setup

1. Install PostgreSQL if not already installed
```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# For MacOS using Homebrew
brew install postgresql

# For Windows
# Download and install from https://www.postgresql.org/download/windows/
```

2. Start PostgreSQL service
```bash
# For Ubuntu/Debian
sudo systemctl start postgresql
sudo systemctl enable postgresql

# For MacOS
brew services start postgresql

# For Windows
# PostgreSQL is automatically started as a service
```

3. Create Database and User
```bash
# Access PostgreSQL prompt
sudo -u postgres psql

# In PostgreSQL prompt
CREATE DATABASE university_db;
CREATE USER university_user WITH PASSWORD 'your_password';
ALTER ROLE university_user SET client_encoding TO 'utf8';
ALTER ROLE university_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE university_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE university_db TO university_user;
GRANT ALL ON SCHEMA public TO university_user;
\q
```

## Project Configuration

1. Create a `.env` file in the project root directory:
```bash
touch .env
```

2. Add the following environment variables to the `.env` file:
```
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=university_db
DB_USER=university_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Database Migration

Run the following commands to create and apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Create Superuser

Create an admin user to access the Django admin interface:
```bash
python manage.py createsuperuser
```

## Running the Development Server

Start the development server:
```bash
python manage.py runserver
```

The application will be available at:
- Main application: http://127.0.0.1:8000/system/
- Admin interface: http://127.0.0.1:8000/admin/

## Project Structure
```
university_system/               
├── student_management/          
│   ├── migrations/              
│   ├── templates/               
│   │   ├── student_management/  
│   │   │   ├── base.html       
│   │   │   ├── student_dashboard.html
│   │   │   ├── admin_dashboard.html
│   │   │   ├── manage_courses.html
│   │   │   ├── enroll_student.html
│   │   │   ├── assign_grade.html
│   │   │   └── login.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── university_system/           
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
