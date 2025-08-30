from rest_framework import serializers
from .models import BasicUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles password hashing.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = BasicUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        """
        Create and return a new user with a hashed password.
        """
        user = BasicUser.objects.create_user(**validated_data)
        return user
