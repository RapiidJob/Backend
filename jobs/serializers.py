from rest_framework import serializers
from .models import Job, JobAddress, JobPostPhoto, JobCategory, JobSubcategory

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

class JobSerializer(serializers.ModelSerializer):
    subcategory = JobSubcategorySerializer(read_only=True, required=False)
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=JobSubcategory.objects.all(), source='subcategory', write_only=True, required=False
    )
    posted_by = serializers.PrimaryKeyRelatedField(read_only=True)
    post_photos = JobPostPhotoSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'subcategory', 'subcategory_id', 'posted_by', 
                  'created_at', 'updated_at', 'post_photos', 'is_finished']

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