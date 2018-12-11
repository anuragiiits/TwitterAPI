from django.shortcuts import render
from django.conf import settings
from django.db import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer

class AddUser(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """Return the details of the current Logged In User"""
        try:
            user = request.user
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        except:
            return Response(
                {
                    "error": ["Authentication details are not correct."]
                },
                status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        """Create a New User profile | Data parameters: email, password, first_name(optional), last_name(optional)"""

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()               #invokes create function defined in serializer class
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {
                    "error": ["username is already taken"]
                },
                status=status.HTTP_400_BAD_REQUEST)
