from rest_framework import serializers
from .models import Job, JobAddress, JobPostPhoto, JobCategory, JobSubcategory

class JobAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAddress
        fields = '__all__'
        read_only_fields = ('created_at', )
        extra_kwargs = {
            'latitude': {'required': False},
            'longitude': {'required': False}
        }

class JobPostPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostPhoto
        fields = '__all__'

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'

class JobSubcategorySerializer(serializers.ModelSerializer):
    category = JobCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=JobCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = JobSubcategory
        fields = ['id', 'category', 'category_id', 'name', 'description']

class JobSerializer(serializers.ModelSerializer):
    subcategory = JobSubcategorySerializer(read_only=True, required=False)
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=JobSubcategory.objects.all(), source='subcategory', write_only=True, required=False
    )
    posted_by = serializers.PrimaryKeyRelatedField(read_only=True)
    job_address = JobAddressSerializer(required=False)
    post_photos = JobPostPhotoSerializer(many=True, read_only=True, required=False)  # Read-only for listing photos

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'subcategory', 'subcategory_id', 'posted_by', 
                  'created_at', 'updated_at', 'job_address', 'post_photos', 'is_finished']

    def create(self, validated_data):
        user = self.context['request'].user
        job_address_data = validated_data.pop('job_address', None)
        post_photos_data = self.context['request'].FILES.getlist('post_photos')  # Handle multiple files
        job = Job.objects.create(posted_by=user, **validated_data)
        
        if job_address_data:
            job_address = JobAddress.objects.create(**job_address_data)
            job.job_address = job_address
        
        for photo_data in post_photos_data:
            created = JobPostPhoto.objects.create(image=photo_data)  
            # Link photo to job
            if created:
                job.post_photos.add(created)

        job.save()
        return job

    def update(self, instance, validated_data):
        job_address_data = validated_data.pop('job_address', None)
        post_photos_data = self.context['request'].FILES.getlist('post_photos')  # Handle multiple files
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if job_address_data:
            if instance.job_address:
                for attr, value in job_address_data.items():
                    setattr(instance.job_address, attr, value)
                instance.job_address.save()
            else:
                job_address = JobAddress.objects.create(**job_address_data)
                instance.job_address = job_address
        
        instance.post_photos.clear()  # Clear existing photos
        for photo_data in post_photos_data:
            JobPostPhoto.objects.create(job=instance, image=photo_data)  # Link photo to job
        
        instance.save()
        return instance
