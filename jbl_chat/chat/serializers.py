from email import message
from rest_framework import serializers
from django.contrib.auth.models import User

from . import models


class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    username = serializers.CharField(max_length=200)


class MessageSerializer(serializers.Serializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    message = serializers.CharField(min_length=1, max_length=100)
    ctime = serializers.DateTimeField()


class CreateMessageSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()
    message = serializers.CharField(min_length=1, max_length=100)

    def create(self, validated_data):
        return models.Message.objects.create(**validated_data)