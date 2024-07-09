<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Rapid Job Backend</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: #333;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        ul li {
            padding: 5px 0;
        }
        code {
            background: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
        }
    </style>
</head>
<body>

    <h1>Rapid Job Backend</h1>
    <p>Welcome to the Rapid Job Backend repository. This project aims to create a platform connecting blue-collar workers with employers, facilitating job postings and applications in Ethiopia. The backend is built using Django and Django REST Framework (DRF).</p>

    <h2>Table of Contents</h2>
    <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#getting-started">Getting Started</a></li>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#running-the-project">Running the Project</a></li>
        <li><a href="#api-endpoints">API Endpoints</a></li>
        <li><a href="#contributing">Contributing</a></li>
    </ul>

    <h2 id="features">Features</h2>
    <ul>
        <li>🔒 User Authentication (Registration, Login, Logout)</li>
        <li>👥 User Profiles (Employer and Worker)</li>
        <li>📄 Job Postings</li>
        <li>📝 Job Applications</li>
        <li>💬 Messaging System</li>
        <li>📊 Work History Tracking</li>
    </ul>

    <h2 id="getting-started">Getting Started</h2>
    <h3 id="prerequisites">Prerequisites</h3>
    <p>Before you begin, ensure you have met the following requirements:</p>
    <ul>
        <li>Python 3.8+</li>
        <li>Django 3.2+</li>
        <li>PostgreSQL</li>
    </ul>

    <h2 id="installation">Installation</h2>
    <h3>Clone the Repository</h3>
    <pre><code>git clone https://github.com/RapiidJob/Backend.git
cd Backend</code></pre>

    <h3>Create a Virtual Environment</h3>
    <pre><code>python3 -m venv venv
source venv/bin/activate</code></pre>

    <h3>Install Dependencies</h3>
    <pre><code>pip install -r requirements.txt</code></pre>

    <h3>Set Up the Database</h3>

    <h3>Run Migrations</h3>
    <pre><code>python manage.py makemigrations
python manage.py migrate</code></pre>

    <h3>Create a Superuser</h3>
    <pre><code>python manage.py createsuperuser</code></pre>

    <h2 id="running-the-project">Running the Project</h2>
    <h3>Start the Development Server</h3>
    <pre><code>python manage.py runserver</code></pre>

    <h3>Access the Application</h3>
    <p>Open your browser and go to <a href="http://127.0.0.1:8000/swagger">http://127.0.0.1:8000/swagger</a>.</p>

    <h2 id="api-endpoints">API Endpoints</h2>
    <p>Here are some of the main API endpoints:</p>
    <ul>
        <li>User Registration: <code>POST /api/auth/register/</code></li>
        <li>User Login: <code>POST /api/auth/login/</code></li>
        <li>Job Postings: <code>GET /api/jobs/</code> | <code>POST /api/jobs/</code></li>
        <li>Job Applications: <code>GET /api/applications/</code> | <code>POST /api/applications/</code></li>
        <li>Messages: <code>GET /api/messages/</code> | <code>POST /api/messages/</code></li>
    </ul>
    <p>For detailed API documentation, visit the Swagger UI at <a href="http://127.0.0.1:8000/swagger">http://127.0.0.1:8000/swagger</a>.</p>

    <h2 id="contributing">Contributing</h2>
    <ol>
        <li>Fork the repository.</li>
        <li>Create a new branch: <code>git checkout -b feature-branch</code>.</li>
        <li>Make your changes.</li>
        <li>Commit your changes: <code>git commit -m 'Add some feature'</code>.</li>
        <li>Push to the branch: <code>git push origin feature-branch</code>.</li>
        <li>Open a Pull Request.</li>
    </ol>

</body>
</html>
