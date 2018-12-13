from django.shortcuts import render
from django.conf import settings
from django.db import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserProfileSerializer, TweetSerializer
from .models import UserProfile, Tweet


class Followers(APIView):
    serializer_class = UserProfileSerializer

    def get(self, request):
        """Get the list of his followings"""

        user_profile = UserProfile.objects.get(user__id=request.user.id)
        serializer=self.serializer_class(user_profile)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Adds the follower to Users profile"""

        try:
            if request.user.email == request.data.get("follow_email"):
                return Response({"error": ["Follow email cannot be same as User email"]},status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(data=request.data, context={"user_email": request.user.email})
            if serializer.is_valid():
                serializer.save()               #invokes create function defined in serializer class
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": ["an error occured"]},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """Removes the follower from Users profile"""

        try:
            user_profile = UserProfile.objects.get(user__id=request.user.id)
            serializer = self.serializer_class(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": ["an error occured"]},status=status.HTTP_400_BAD_REQUEST)


class TweetHandling(APIView):
    serializer_class = TweetSerializer

    def get(self, request):
        """Get all the tweets created by the current logged in user"""

        tweets = Tweet.objects.filter(created_by__id=request.user.id)
        serializer=self.serializer_class(tweets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Creates a new Tweet"""

        try:
            serializer = self.serializer_class(data=request.data, context={"user_email": request.user.email})
            if serializer.is_valid():
                serializer.save()               #invokes create function defined in serializer class
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": ["an error occured"]},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """Deletes a Tweet"""

        try:
            tweet_id = request.data.get('id')
            if tweet_id is None:
                return Response(status=status.HTTP_206_PARTIAL_CONTENT)
            tweet = Tweet.objects.get(id=tweet_id)
            if request.user.id == tweet.created_by.id:
                tweet.delete()
                return Response(status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({"error": ["an error occured"]},status=status.HTTP_400_BAD_REQUEST)


class AllTweetsHandling(APIView):
    serializer_class = TweetSerializer

    def get(self, request):
        """Get all the tweets that could be viewed by the current user(except his own tweets)"""

        user_profile = UserProfile.objects.get(user__id=request.user.id)
        followings = user_profile.following.all()
        all_tweets = Tweet.objects.none()
        for user in followings:
            tweets = Tweet.objects.filter(created_by=user)
            all_tweets = all_tweets | tweets
        all_tweets = all_tweets.order_by('-created_time')
        serializer=self.serializer_class(all_tweets, many=True)
        return Response(serializer.data)
