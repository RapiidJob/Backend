import requests
from getpass import getpass
import random

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwOTQzNDkyLCJpYXQiOjE3MjA2NDM0OTIsImp0aSI6IjE2ZGY5OWQ4MDI4MTQzYzhhNWJkYmJmMjBjMjE0NWY0IiwidXNlcl9pZCI6NX0.QiHMKQkHh83xlluvevBHu7fiU4ULinOfF2VTMP2LNP8"
endpoint = "http://127.0.0.1:8000/api/jobs/search_by_location/"


import math

def get_random_point_within_radius(latitude, longitude, radius_km):
    # Earth's average radius in kilometers
    earth_radius_km = 6371
    
    # Convert latitude and longitude to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)
    
    # Calculate the circumference of the circle in kilometers
    circumference_km = 2 * math.pi * earth_radius_km
    
    # Generate a random angle for the point within the circle
    angle_deg = random.randint(0, 360) * 360
    
    # Convert the angle to radians
    angle_rad = math.radians(angle_deg)
    
    # Calculate the x and y coordinates of the point
    x = earth_radius_km + radius_km
    y = math.sqrt(x**2 - radius_km**2)
    
    # Calculate the final x and y coordinates
    final_x = x * math.cos(angle_rad)
    final_y = y * math.sin(angle_rad)
    
    # Convert the x and y coordinates back to latitude and longitude
    final_lat = math.degrees(math.atan(final_y / final_x))
    final_lon = lon_rad + math.degrees(final_x / (earth_radius_km + radius_km))
    
    return final_lat, final_lon

given_latitude = 12.033000
given_longitude = 40.012000

radius_km = 5

random_latitude, random_longitude = get_random_point_within_radius(given_latitude, given_longitude, radius_km)

print(f"Random point within 5km:\nLatitude: {random_latitude}\nLongitude: {random_longitude}")


data = {
    'country': 'Ethiopia',
    'city': 'Addis Ababa',
    'region': 'Addis Ababa',
    'category': 'Maintenance & Repair',  
    'title':   'Electrician Needed',
    'latitude':random_latitude,
    'longitude': random_longitude,
}

headers = {
    "Authorization" : f"Bearer {token}"
}

get_response = requests.post(endpoint, headers=headers, data=data)
print(get_response.json())


