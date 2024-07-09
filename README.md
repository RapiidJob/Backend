# Rapid Job Backend

Welcome to the Rapid Job Backend repository. This project aims to create a platform connecting blue-collar workers with employers, facilitating job postings and applications in Ethiopia. The backend is built using Django and Django REST Framework (DRF).

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)

## Features
- 🔒 User Authentication (Registration, Login, Logout)
- 👥 User Profiles (Employer and Worker)
- 📄 Job Postings
- 📝 Job Applications
- 💬 Messaging System
- 📊 Work History Tracking

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8+
- Django 3.2+
- PostgreSQL

### Installation

1. **Clone the Repository**
    ```sh
    git clone https://github.com/RapiidJob/Backend.git
    cd Backend
    ```

2. **Create a Virtual Environment**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up the Database**

5. **Run Migrations**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser**
    ```sh
    python manage.py createsuperuser
    ```

## Running the Project

**Start the Development Server**
```sh
python manage.py runserver
