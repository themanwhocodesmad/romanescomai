from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.models import CustomUser
from .models import Customer, JobCard, Image


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


# Change Password
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class JobCardSerializerForJobCreation(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = JobCard
        exclude = ['job_number']  # Exclude job_number from serialization

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        customer, created = Customer.objects.get_or_create(**customer_data)
        job_card = JobCard.objects.create(customer=customer, **validated_data)
        return job_card



class JobCardSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = JobCard
        fields = '__all__'

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        # Only create a new customer if it doesn't already exist
        customer, created = Customer.objects.get_or_create(**customer_data)
        job_card = JobCard.objects.create(customer=customer, **validated_data)
        return job_card


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
