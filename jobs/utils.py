from .models import JobAddress
def create_job_address_from_user(user):
    job_address = JobAddress.objects.create(city=user.address.city, region=user.address.region, country=user.address.country, Latitude=user.address.latitude, Longitude=user.address.Longitude)
    return job_address
