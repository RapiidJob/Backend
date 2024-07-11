from .models import JobAddress
import math
def create_job_address_from_user(user):
    job_address = JobAddress.objects.create(city=user.address.city, region=user.address.region, country=user.address.country, Latitude=user.address.latitude, Longitude=user.address.Longitude)
    return job_address



def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    print(lat1, lat2)
    lat1 = float(lat1)
    lat2 = float(lat2)

    lon1 = float(lon1)
    lon2 = float(lon2)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c 