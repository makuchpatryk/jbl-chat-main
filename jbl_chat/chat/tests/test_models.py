from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError

from chat.models import Message


class ModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="pat", password="pass")
        self.user2 = User.objects.create(username="mak", password="pass1")

    def test_message_creation(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, message="this is test")
        self.assertTrue(isinstance(msg, Message))
        self.assertEqual(msg.__str__(), msg.message)

    def test_message_empty_message(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, message="")
        self.assertTrue(isinstance(msg, Message))
        self.assertEqual(msg.__str__(), msg.message)
        self.assertEqual(msg.message, '')

    def test_message_without_sender(self):
        with self.assertRaises(IntegrityError):
            Message.objects.create(sender=None, receiver=self.user2, message="test text")

    def test_message_without_receiver(self):
        with self.assertRaises(IntegrityError):
            Message.objects.create(sender=self.user1, receiver=None, message="test text")
    
    def test_message_without_users(self):
        with self.assertRaises(IntegrityError):
            Message.objects.create(sender=None, receiver=None, message="test text")

    def test_messages_count(self):
        Message.objects.create(sender=self.user1, receiver=self.user2, message="this is test 1")
        Message.objects.create(sender=self.user1, receiver=self.user2, message="this is test 2")
        Message.objects.create(sender=self.user1, receiver=self.user2, message="this is test 3")
        all_count = Message.objects.all().count()

        self.assertEqual(all_count, 3)