from typing import Dict, Any
from rest_framework.serializers import ModelSerializer, Serializer
from user.models import User, OTPModel, UserInfo
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login


class UserModelSerializer(ModelSerializer):
    """
    Serializer for the User model.

    This serializer handles user creation, setting the password securely, and marking the user as inactive by default.
    """
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        """
        Method to create a new user instance.

        This method sets the user's password securely and marks the user as inactive by default.

        Args:
            validated_data (dict): Validated data for user creation.

        Returns:
            User: The newly created user instance.
        """
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user


class OTPSerializer(ModelSerializer):
    """
    Serializer for the OTPModel.
    """
    class Meta:
        model = OTPModel
        fields = ['email', 'otp']


class EmailSerializer(Serializer):
    """
    Serializer for handling email data.
    """
    email = serializers.EmailField()


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining JWT tokens for users.

    This serializer extends the TokenObtainPairSerializer provided by Django REST Framework SimpleJWT.

    It overrides the validate method to update the last login timestamp of the user upon successful token generation.
    """
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        """
        Method to validate token data and update last login timestamp.

        Args:
            attrs (dict): Token data attributes.

        Returns:
            dict: Validated token data.
        """
        data = super().validate(attrs)
        update_last_login(None, self.user)
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    """Serializer for UserInfo model."""
    class Meta:
        model = UserInfo
        fields = '__all__'


