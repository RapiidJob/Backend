from rest_framework import serializers
from .models import CustomUser, WorkerProfile, EmployerProfile, UserAddress

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
        fields = ("email", "password")
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
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
    address = UserAddressSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'birth_date', 'gender', 'phone_number',
                  'verification_type', 'verification_document', 'profile_image', 'address',
                  'is_worker', 'is_employer', 'is_admin', 'is_identity_verified',
                  'is_email_verified', 'is_phone_verified', 'rating', 'created_at')
        read_only_fields = ('email', 'created_at', 'is_identity_verified', 'is_email_verified', 'is_phone_verified', 'rating', 'password')

        extra_kwargs = {
            'profile_image': {'required': False},
            'verification_document': {'required': False}
        }

    # def create(self, validated_data):
    #     address_data = validated_data.pop('address', None)
    #     user = CustomUser.objects.create(**validated_data)
    #     if address_data:
    #         created = UserAddress.objects.create(**address_data)
    #         user.address = created
    #     return user

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        instance = super().update(instance, validated_data)
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
        return instance


class EmployerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = EmployerProfile
        fields = ('id', 'user', 'plan', 'last_paid')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        user_instance = self.context['request'].user  # Retrieve current user from request

        # Update user instance with provided data
        user_serializer = CustomUserSerializer(instance=user_instance, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()

        # Create EmployerProfile instance with updated user and other validated data
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
        instance.last_paid = validated_data.get('last_paid', instance.last_paid)
        instance.user = user_instance
        instance.save()

        return instance


class WorkerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = WorkerProfile
        fields = ('id', 'user', 'plan', 'prefered_job_categories', 'last_applied', 'last_paid')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = CustomUserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        return super().update(instance, validated_data)
