# serializers.py
from rest_framework import serializers
from .models import Application, WorkHistory, WorkInProgress
from jobs.serializers import JobSerializer
from accounts.serializers import CustomUserSerializer

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('job', 'application_letter', 'agreed_price', 'currency_type')

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    worker = CustomUserSerializer()

    class Meta:
        model = Application
        fields = ('id', 'job', 'worker', 'application_letter', 'application_date_time', 'status', 'agreed_price', 'currency_type')
        read_only_fields = ('application_date_time', 'status')

class WorkHistorySerializer(serializers.ModelSerializer):
    job = JobSerializer()
    worker = CustomUserSerializer()
    application = ApplicationSerializer()

    class Meta:
        model = WorkHistory
        fields = ('id', 'job', 'worker', 'application', 'created_at', 'description', 'paid_price', 'currency_type', 'score', 'was_paid')
        read_only_fields = ('created_at',)

class WorkinProgressSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only = True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = WorkInProgress
        fields = [
            'id', 'job', 'application', 'started_at', 'is_finished'
        ]
    
    def create(self, validated_data):
        return super().create(validated_data)