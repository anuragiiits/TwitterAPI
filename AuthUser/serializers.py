from rest_framework import serializers
from django.conf import settings

from .models import User
from TwitterCore.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user_profile = UserProfile(user=user)
        user_profile.save()
        return user
