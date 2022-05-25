from functools import partial
from django.http import request
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (LoginSerializer, 
    UserSerializer, ChangePasswordSerializer, UpdateUserProfileSerilaizer)
from django.conf import settings
from django.contrib.auth import authenticate
import jwt

# Create your views here.
class SignupView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': 'created',
                'data': serializer.data
            }
            return Response(data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token = jwt.encode({"username": username}, settings.JWT_SECRET_KEY, algorithm="HS256")
                
                
                data = {
                    'status': 'Successful',
                    'data': serializer.data,
                    'token': token
                }
                return Response(data, status.HTTP_200_OK)
            return Response({"details": "Invalid Credentials"},status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data.get('old_password'))
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Wrong password"]}, status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            data = {
                'status': 'Successful',
                'data': [],
                'message': 'Password Updated Successfully'
            }
            return Response(data, status.HTTP_200_OK)

class UpdateUserProfileView(generics.GenericAPIView):
    serializer_class = UpdateUserProfileSerilaizer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UpdateUserProfileSerilaizer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            data = {
                'status': 'Successful',
                'data': serializer.data,
                'message': 'Profile Updated Successfully'
            }
            if 'username' in serializer.validated_data:
                username = serializer.validated_data.get('username')
                data['message'] = 'Profile Updated Successfully. Use the new token for authentication'
                data['new_token'] = jwt.encode({"username": username}, settings.JWT_SECRET_KEY, algorithm="HS256")
            return Response(data, status.HTTP_200_OK)

