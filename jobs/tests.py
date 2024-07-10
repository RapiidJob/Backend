from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Job, JobCategory, JobSubcategory, JobAddress, JobPostPhoto
from django.contrib.auth import get_user_model
from io import BytesIO
from PIL import Image

User = get_user_model()

def create_image():
    file = BytesIO()
    image = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file

class JobCreateTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='employer@gmail.com', password='password', account_type='Employer')
        self.category = JobCategory.objects.create(name='Test Category', description='Test Description')
        self.subcategory = JobSubcategory.objects.create(category=self.category, name='Test Subcategory', description='Test Description')
        self.address_data = {
            "street": "123 Test Street",
            "city": "Test City",
            "state": "Test State",
            "postal_code": "12345",
            "country": "Test Country",
            "latitude": "0.0000",
            "longitude": "0.0000"
        }
        self.client.login(username='employer', password='password')

    def test_create_job(self):
        url = reverse('job-create')  # Ensure this matches your URL name
        image1 = open(r'C:/Users/Abdi/Downloads/test.png', 'rb')
        image2 = open(r'C:/Users/Abdi/Downloads/test.png', 'rb')

        data = {
            "title": "Test Job",
            "description": "Test Description",
            "subcategory_id": self.subcategory.id,
            "job_address": self.address_data,
            "post_photos": [image1, image2]
        }
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(JobPostPhoto.objects.count(), 2)

        job = Job.objects.first()
        self.assertEqual(job.title, "Test Job")
        self.assertEqual(job.description, "Test Description")
        self.assertEqual(job.subcategory, self.subcategory)
        self.assertEqual(job.posted_by, self.user)
        self.assertIsNotNone(job.job_address)
        self.assertEqual(job.post_photos.count(), 2)
