import os
import django
from django.db import transaction
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RapidJob.settings')
django.setup()

from jobs.models import JobCategory, JobSubcategory

categories = [
    ("Maintenance & Repair", [
        "Plumbing Services",
        "Electrical Services",
        "Appliance Repair",
        "HVAC Services",
        "General Handyman Services",
    ]),
    ("Construction & Renovation", [
        "Masonry Work",
        "Carpentry Services",
        "Painting Services",
        "Roofing Services",
        "Flooring Installation",
    ]),
    ("Household Services", [
        "Cleaning Services",
        "Laundry Services",
        "House Sitting Services",
        "Pet Sitting Services",
    ]),
    ("Transport & Delivery", [
        "Delivery Services",
        "Moving Services",
        "Transportation Services",
    ]),
    ("Education & Tutoring", [
        "Tutoring Services",
        "Exam Preparation Classes",
        "Music Lessons",
        "Computer Skills Training",
    ]),
    ("Gardening & Landscaping", [
        "Gardening Services",
        "Landscaping Design",
        "Tree Trimming and Removal",
    ]),
    ("Health & Wellness", [
        "Personal Fitness Training",
        "Yoga and Meditation Classes",
        "Massage Therapy",
    ]),
    ("Event Services", [
        "Event Planning",
        "Catering Services",
        "Photography Services",
        "DJ Services",
        "Event Setup and Cleanup",
    ])
]

# Function to add categories and subcategories
def add_categories_and_subcategories():
    with transaction.atomic():
        for category_name, subcategories in categories:
            category, created = JobCategory.objects.get_or_create(name=category_name)
            if created:
                print(f"Created category: {category_name}")
            for subcategory_name in subcategories:
                subcategory, sub_created = JobSubcategory.objects.get_or_create(
                    category=category,
                    name=subcategory_name
                )
                if sub_created:
                    print(f"  Created subcategory: {subcategory_name} under category {category_name}")


add_categories_and_subcategories()
