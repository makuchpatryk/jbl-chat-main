import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework import status

from . import serializers
from . import models


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({
                "error": "Please enter both username and password" }, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"detail": "Success"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response('Success', status=status.HTTP_200_OK)


class Users(APIView):
    def get(self, request):
        users = User.objects.exclude(pk=request.user.pk)
        serializer = serializers.UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class Message(APIView):
    def get(self, request, receiver_id):
        """
            get all message with this user
        """
        if request.user.pk == receiver_id:
            return Response(
                {"error": "You're not able to see messages to myself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(pk=receiver_id)
        except ValueError:
            return Response(
                {"error": "Please enter number receiver id."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                {"error": "Please enter correct receiver id."}, status=status.HTTP_400_BAD_REQUEST)

        messages = models.Message.objects.filter(sender=request.user, receiver=receiver)

        serializer = serializers.MessageSerializer(
            messages, many=True, context={'request': request})
        return Response(serializer.data, status=200)

    def post(self, request, receiver_id):
        """
        sending message to user 
        """
        context = {}
        context['message'] = request.data.get('message', '')

        if request.user.pk == receiver_id:
            return Response(
                {"error": "You're not able to send messages to myself."}, status=status.HTTP_400_BAD_REQUEST)

        context['sender_id'] = request.user.pk
        context['receiver_id'] = receiver_id

        serializer = serializers.CreateMessageSerializer(data=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
