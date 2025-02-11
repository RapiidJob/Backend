from rest_framework import serializers
from .models import Job, JobAddress, JobPostPhoto, JobCategory, JobSubcategory, UserSavedJob
from accounts.serializers import CustomUserSerializer

class JobAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAddress
        fields = '__all__'
        read_only_fields = ('created_at', )

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

class JobSubCatagorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSubcategory
        fields = ['id', 'name', 'description']
        
class JobCatagoryReadSerializer(serializers.ModelSerializer):
    subcategories = JobSubCatagorReadSerializer(many=True, read_only=True)
    class Meta:
        model = JobCategory
        fields = ['id', 'name', 'description', 'subcategories']
    
class JobSerializer(serializers.ModelSerializer):
    subcategory = JobSubcategorySerializer(read_only=True, required=False)
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=JobSubcategory.objects.all(), source='subcategory', write_only=True, required=False
    )
    posted_by = CustomUserSerializer(read_only=True)
    post_photos = JobPostPhotoSerializer(many=True, read_only=True, required=False)
    job_address = JobAddressSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'subcategory', 'subcategory_id', 'posted_by', 
                  'created_at', 'updated_at', 'post_photos', 'is_finished', 'job_address', "estimated_price", "currency_type"]

    def create(self, validated_data):
        user = self.context['request'].user

        post_photos_data = self.context['request'].FILES.getlist('post_photos')

        job = Job.objects.create(posted_by=user, **validated_data)
        for photo_data in post_photos_data:
            created = JobPostPhoto.objects.create(image=photo_data)
            if created:
                job.post_photos.add(created)

        job.save()
        return job

    def update(self, instance, validated_data):
        post_photos_data = self.context['request'].FILES.getlist('post_photos')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.post_photos.clear()
        for photo_data in post_photos_data:
            JobPostPhoto.objects.create(job=instance, image=photo_data)

        instance.save()
        return instance


class SavedJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), source='job', write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = UserSavedJob
        fields = ['id', 'user', 'job', 'job_id', 'created_at']
        
        
