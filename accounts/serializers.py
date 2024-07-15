from rest_framework import serializers
from .models import CustomUser, WorkerProfile, EmployerProfile, UserAddress
from django.contrib.auth import authenticate

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
        read_only_fields = ('created_at', )

        extra_kwargs = {
            'latitude': {'required': False},
            
            'longitude': {'required': False}
        }

#for first time user is created via email and password only
class CustomUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name","account_type", "middle_name", "last_name", "phone_number", "profile_image")
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        type = validated_data.pop("user_type", None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
# class CustomUserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'email', 'password', 'first_name', 'last_name', 'birth_date', 'gender', 'phone_number',
#                   'verification_type', 'verification_document', 'profile_image', 'address')
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             birth_date=validated_data['birth_date'],
#             gender=validated_data['gender'],
#             phone_number=validated_data['phone_number'],
#             verification_type=validated_data['verification_type'],
#             verification_document=validated_data['verification_document'],
#             profile_image=validated_data.get('profile_image', None),
#             address=validated_data.get('address', None),
#         )
#         return user
    

#address and other user details is created when user is updated
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'birth_date', 'gender', 'phone_number',
                  'verification_type', 'verification_document', 'profile_image', 'address',
                  "account_type", 'is_identity_verified',
                  'is_email_verified', 'is_phone_verified', 'rating', 'created_at')
        read_only_fields = ('email', 'created_at','is_email_verified', 'is_identity_verified', 'is_phone_verified', 'rating', 'password')

        extra_kwargs = {
            'profile_image': {'required': False},
            'verification_document': {'required': False}
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.user.account_type == 'Admin':
            self.fields['is_identity_verified'].read_only = False
            self.fields['is_email_verified'].read_only = False
            self.fields['is_phone_verified'].read_only = False
        if request and request.user.account_type == 'Employer' and 'rating' in request.data:
            self.fields['rating'].read_only = False


    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        request = self.context.get('request', None)
        if request and request.user.account_type == 'Admin':
            instance.is_identity_verified = validated_data.get('is_identity_verified', None)
            instance.is_email_verified = validated_data.get('is_email_verified', None)
            instance.is_phone_verified = validated_data.get('is_phone_verified', None)
            return super().update(instance, validated_data)
        if request and request.user.account_type == 'Employer' and 'rating' in request.data:
            instance.rating = validated_data.get('rating', instance.rating)
            if instance.rating:
                return super().update(instance, validated_data)
            else:
                raise Exception('rating None')
        
        address_data = validated_data.pop('address', None)
        if address_data:
            if hasattr(instance, 'address') and instance.address:
                instance.address.street = address_data.get('street', instance.address.street)
                instance.address.city = address_data.get('city', instance.address.city)
                instance.address.state = address_data.get('state', instance.address.state)
                instance.address.zipcode = address_data.get('zipcode', instance.address.zipcode)
                instance.address.save()
            else:
                created = UserAddress.objects.create(**address_data)
                instance.address = created
                instance.save()
        
        return instance


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ('id', 'plan', 'jobs_completed')
    
    def create(self, validated_data):
        user_instance = self.context['request'].user 
        if user_instance.account_type != "Employer":
            raise serializers.ValidationError("User is not an employer")
        validated_data.pop('user', {})
        employer_instance = EmployerProfile.objects.create(user=user_instance, **validated_data)
        return employer_instance
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_instance = instance.user  # Retrieve current user from EmployerProfile instance

        # Update user instance with provided data
        user_serializer = CustomUserSerializer(instance=user_instance, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()

        # Update EmployerProfile instance with validated data
        instance.plan = validated_data.get('plan', instance.plan)
        # instance.last_paid = validated_data.get('last_paid', instance.last_paid)
        instance.user = user_instance
        instance.save()

        return instance


class WorkerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerProfile
        fields = ('id', 'plan')
        
    
    def create(self, validated_data):
        user_instance = self.context['request'].user  # Retrieve current user from request
        if user_instance.account_type != "Worker":
            return None
        validated_data.pop('user', {})
        worker_instance = WorkerProfile.objects.create(user=user_instance, **validated_data)
        return worker_instance

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_instance = instance.user  # Retrieve current user from Workers instance
        # Update user instance with provided data
        user_serializer = CustomUserSerializer(instance=user_instance, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()

        # Update Workers instance with validated data
        instance.plan = validated_data.get('plan', instance.plan)
        # instance.last_paid = validated_data.get('last_paid', instance.last_paid)
        instance.user = user_instance
        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Both email and password are required")
        
        data['user'] = user
        return data