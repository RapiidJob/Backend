import os
import requests

# Get the absolute path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# API endpoint for creating jobs (replace with your actual endpoint)
REGISTRATION_URL = 'http://127.0.0.1:8000/accounts/register/'

# User data and profile file
user_data = {
    'phone_number': '123456789',
    'password': '123456789_',
    'gender': 'Female', 
    'first_name': 'abdu',
    'middle_name': 'hussen',
    'last_name': 'Ali',
    'email': 'testuser@example.com',
    'account_type': "Employer",
}

# Specify the absolute path to the profile image
profile_files = {
    'profile_image': open(os.path.join(script_dir, 'profile.png'), 'rb'),
    'verification_document': open(os.path.join(script_dir, 'jobpost.png'), 'rb'),
}

# Make the registration request
registration_response = requests.post(REGISTRATION_URL, data=user_data)
print(registration_response.json())

if registration_response.status_code == 201:
    employer_profile_url = "http://127.0.0.1:8000/accounts/employer/create/"
    token = registration_response.json()['token']['access']
    
    employer_data = {
    }
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(employer_profile_url, data=employer_data,files=profile_files, headers=headers)
    
    
# Close the file handle



API_URL = 'http://127.0.0.1:8000/jobs/create/'

if registration_response.status_code == 201:
    BEARER_TOKEN = registration_response.json()['token']['access']

    # Dummy data for jobs
    dummy_jobs = [
        
        {
            'title': 'Plumber Needed',
            'description': 'Looking for an experienced plumber to fix leaky pipes.',
            'subcategory_id': 1,  # Replace with actual subcategory ID
                'country': 'Ethiopia',
                'city': 'Addis Ababa',
                'region': 'Addis Ababa',
                'latitude': 9.02045,
                'longitude': 38.75278,
                
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                },
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False
        },
        {
            'title': 'Electrician Needed',
            'description': 'Electrical wiring repair needed for a residential building.',
            'subcategory_id': 2,  # Replace with actual subcategory ID
                'country': 'Ethiopia',
                'city': 'Addis Ababa',
                'region': 'Addis Ababa',
                'latitude': 9.02045,
                'longitude': 38.75278,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False
        },
    ]

    # Function to send jobs data to API
    def send_jobs_data(jobs):
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }
        for job_data in jobs:
            files = []
            for photo_data in job_data.pop('post_photos', []):
                files.append(('post_photos', photo_data['image']))
            
            response = requests.post(API_URL, data=job_data, files=files, headers=headers)
            if response.status_code == 201:
                print(f"Job created successfully: {response.json()}")
            else:
                print(f"Failed to create job: {response.status_code}, {response.json()}")

    # Example usage: Send dummy jobs data to the API
    send_jobs_data(dummy_jobs)
