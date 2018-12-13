from rest_framework import serializers
from django.conf import settings

from AuthUser.models import User
from .models import UserProfile, Tweet


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email"]


class UserProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    follow_email = serializers.EmailField(write_only=True)
    following = UserSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user_email", "follow_email", "following"]

    def create(self, validated_data):
        user_email = self.context.get("user_email")
        follow_email = validated_data.get("follow_email")
        user_profile = UserProfile.objects.get(user__email=user_email)
        follow = User.objects.get(email=follow_email)
        user_profile.following.add(follow)
        user_profile.save()
        return user_profile

    def update(self, instance, validated_data):
        unfollow_email = validated_data.get("follow_email")
        unfollow = User.objects.get(email=unfollow_email)
        instance.following.remove(unfollow)
        instance.save()
        return instance


class TweetSerializer(serializers.ModelSerializer):
    created_by = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta:
        model = Tweet
        fields = ["id", "created_by", "tweet", "created_time"]

    def create(self, validated_data):
        user_email = self.context.get("user_email")
        user =  User.objects.get(email=user_email)
        return Tweet.objects.create(created_by=user, **validated_data)
