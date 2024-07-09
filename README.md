Rapid Job Backend

Welcome to the Rapid Job Backend repository. This project aims to create a platform connecting blue-collar workers with employers, facilitating job postings and applications in Ethiopia. The backend is built using Django and Django REST Framework (DRF).

Table of Contents
Features
Getting Started
Prerequisites
Installation
Running the Project
API Endpoints
Contributing


Features
🔒 User Authentication (Registration, Login, Logout)
👥 User Profiles (Employer and Worker)
📄 Job Postings
📝 Job Applications
💬 Messaging System
📊 Work History Tracking
Getting Started
Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.8+
Django 3.2+
PostgreSQL
Installation
Clone the Repository


git clone https://github.com/RapiidJob/Backend.git
cd Backend
Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate


Install Dependencies
pip install -r requirements.txt
Set Up the Database


Run Migrations
python manage.py makemigrations
python manage.py migrate


Create a Superuser
python manage.py createsuperuser


Running the Project

Start the Development Server


python manage.py runserver

Access the Application
Open your browser and go to http://127.0.0.1:8000/wagger.

API Endpoints
Here are some of the main API endpoints:

User Registration: POST /api/auth/register/
User Login: POST /api/auth/login/
Job Postings: GET /api/jobs/ | POST /api/jobs/
Job Applications: GET /api/applications/ | POST /api/applications/
Messages: GET /api/messages/ | POST /api/messages/
For detailed API documentation, visit the Swagger UI at http://127.0.0.1:8000/swagger/.

Contributing

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.
