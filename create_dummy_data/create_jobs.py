import os
import requests

# Get the absolute path to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# API endpoint for creating jobs (replace with your actual endpoint)
REGISTRATION_URL = 'http://127.0.0.1:8000/api/accounts/register/'

# User data and profile file
user_data = {
    'phone_number': '123456789',
    'password': '123456789_',
    'gender': 'Female', 
    'first_name': 'abdu',
    'middle_name': 'hussen',
    'last_name': 'Ali',
    'email': 'abdulwahidhussen750@gmail.com',
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
    employer_profile_url = "http://127.0.0.1:8000/api/accounts/employer/create/"
    token = registration_response.json()['token']['access']
    
    employer_data = {
    }
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(employer_profile_url, data=employer_data,files=profile_files, headers=headers)
    
    
# Close the file handle

API_URL = 'http://127.0.0.1:8000/api/jobs/create/'

if registration_response.status_code == 201:
    BEARER_TOKEN = registration_response.json()['token']['access']

    # Dummy data for jobs
    dummy_jobs = [
        {
            'title': "Plumbing Repair",
            'description': 'Looking for an experienced plumber to fix leaky pipes.',
            'subcategory_id': 1,  
            'country': 'Ethiopia',
            'city': 'Adama',
            'region': 'Oromia',
            'latitude': 9.0371,
            'longitude': 38.7469,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 500,
            "payement_choice": "PerTask"
        },
        {
            'title': "Electrical Wiring Repair",
            'description': 'Electrical wiring repair needed for a residential building.',
            'subcategory_id': 2,  
            'country': 'Ethiopia',
            'city': 'Addis Ababa',
            'region': 'Addis Ababa',
            'latitude': 9.0300,
            'longitude': 38.7400,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 300,
            "payement_choice": "PerTask"
        },
        {
            'title': "Appliance Repair",
            'description': 'Need to repair a broken refrigerator.',
            'subcategory_id': 3,  
            'country': 'Ethiopia',
            'city': 'Hawassa',
            'region': 'SNNPR',
            'latitude': 7.0570,
            'longitude': 38.4865,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 700,
            "payement_choice": "PerTask"
        },
        {
            'title': "HVAC Maintenance",
            'description': 'Regular maintenance for an HVAC system.',
            'subcategory_id': 4,  
            'country': 'Ethiopia',
            'city': 'Mekele',
            'region': 'Tigray',
            'latitude': 13.4960,
            'longitude': 39.4753,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 600,
            "payement_choice": "PerTask"
        },
        {
            'title': "General Handyman",
            'description': 'Various small repairs needed around the house.',
            'subcategory_id': 5,  
            'country': 'Ethiopia',
            'city': 'Gondar',
            'region': 'Amhara',
            'latitude': 12.6035,
            'longitude': 37.4521,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 200,
            "payement_choice": "PerTask"
        },
        {
            'title': "House Painting",
            'description': 'Painting services needed for a two-story house.',
            'subcategory_id': 6,  
            'country': 'Ethiopia',
            'city': 'Dire Dawa',
            'region': 'Dire Dawa',
            'latitude': 9.5931,
            'longitude': 41.8661,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 1000,
            "payement_choice": "PerTask"
        },
        {
            'title': "Roofing Services",
            'description': 'Roof repair needed after storm damage.',
            'subcategory_id': 7,  
            'country': 'Ethiopia',
            'city': 'Jimma',
            'region': 'Oromia',
            'latitude': 7.6667,
            'longitude': 36.8333,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 1500,
            "payement_choice": "PerTask"
        },
        {
            'title': "Flooring Installation",
            'description': 'Install new hardwood floors in the living room.',
            'subcategory_id': 8,  
            'country': 'Ethiopia',
            'city': 'Bahir Dar',
            'region': 'Amhara',
            'latitude': 11.5936,
            'longitude': 37.3908,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 2000,
            "payement_choice": "PerTask"
        },
        {
            'title': "House Cleaning",
            'description': 'Need a cleaning service for a 3-bedroom apartment.',
            'subcategory_id': 9,  
            'country': 'Ethiopia',
            'city': 'Harar',
            'region': 'Harari',
            'latitude': 9.3114,
            'longitude': 42.1244,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 400,
            "payement_choice": "PerTask"
        },
        {
            'title': "Transport & Delivery",
            'description': 'Need assistance with moving furniture to a new apartment.',
            'subcategory_id': 15,  
            'country': 'Ethiopia',
            'city': 'Shashamane',
            'region': 'Oromia',
            'latitude': 7.1950,
            'longitude': 38.9936,
            'post_photos': [
                {
                    'image': open(os.path.join(script_dir, 'jobpost.png'), 'rb')  # Replace with actual photo file path
                }
            ],
            'is_finished': False,
            "use_my_address": False,
            "currency_type": "Birr", 
            "estimated_price": 800,
            "payement_choice": "PerTask"
        }
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
