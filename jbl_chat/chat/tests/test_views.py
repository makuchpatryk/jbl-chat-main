import pprint
import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve

from chat import views

class ViewTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="pat")
        user1.set_password('pass')
        user1.save()
        self.user1 = user1

        user2 = User.objects.create(username="mak")
        user2.set_password('pass2')
        user2.save()
        self.user2 = user2

        user3 = User.objects.create(username="joz")
        user3.set_password('pass3')
        user3.save()
        self.user3 = user3

    def test_view_url_exists_without_request_login(self):
        response = self.client.get(reverse('chat:login'))
        self.assertEqual(response.status_code, 405)


    def test_view_url_exists_without_request_logout(self):
        response = self.client.get(reverse('chat:logout'))
        self.assertEqual(response.status_code, 403)


    def test_login(self):
        login = self.client.post(reverse('chat:login'),
            {'username': self.user2.username, 'password': 'pass2'}) 

        self.assertEqual(login.status_code, 200)


    def test_logout(self):
        self.client.post(reverse('chat:login'),
            {'username': self.user1.username, 'password': 'pass'})

        logout = self.client.post(reverse('chat:logout')) 

        self.assertEqual(logout.status_code, 200)

    
    def test_view_url_exists_without_request_users(self):
        response = self.client.get(reverse('chat:users'))
        self.assertEqual(response.status_code, 403)


    def test_view_users(self):
        self.client.post(reverse('chat:login'),
            {'username': self.user1.username, 'password': 'pass'})

        response = self.client.get(reverse('chat:users'))
        self.assertEqual(response.status_code, 200)

        response_content_json = json.loads(response.content)
        self.assertEqual(len(response_content_json), 2)

        author_exists = [True if item['username'] == self.user1.username\
            else False for item in response_content_json]
        self.assertFalse(any(author_exists))


    def test_view_url_exists_without_request_message(self):
        response = self.client.get(reverse('chat:message', kwargs={'receiver_id': 1}))
        self.assertEqual(response.status_code, 403)


    def test_view_url_see_message_to_yourself(self):
        self.client.post(reverse('chat:login'),
            {'username': self.user1.username, 'password': 'pass'})

        response = self.client.get(reverse('chat:message', kwargs={'receiver_id': 1}))

        self.assertEqual(response.status_code, 400)
        response_content_json = json.loads(response.content)

        self.assertEqual(response_content_json['error'], "You're not able to see messages to myself.")


    def test_view_url_send_messages_to_other(self):
        self.client.post(reverse('chat:login'),
            {'username': self.user1.username, 'password': 'pass'})

        self.client.post(reverse('chat:message', kwargs={'receiver_id': 2}),
                                 {'message': 'this is text 1'})
        self.client.post(reverse('chat:message', kwargs={'receiver_id': 2}),
                                 {'message': 'this is text 2'}) 

        response = self.client.get(reverse('chat:message', kwargs={'receiver_id': 2}))
        response_content_json = json.loads(response.content)

        self.assertEqual(len(response_content_json), 2)


    def test_view_url_see_message_to_others(self):
        self.client.post(reverse('chat:login'),
            {'username': self.user1.username, 'password': 'pass'})

        response = self.client.get(reverse('chat:message', kwargs={'receiver_id': 2}))

        self.assertEqual(response.status_code, 200)



    def test_view_url_send_message_to_yourself(self):
        self.client.post(reverse('chat:login'),
            {'username': self.user1.username, 'password': 'pass'})

        response = self.client.post(reverse('chat:message', kwargs={'receiver_id': 1}),
                                 {'message': 'this is text'})  

        self.assertEqual(response.status_code, 400)
        response_content_json = json.loads(response.content)

        self.assertEqual(response_content_json['error'], "You're not able to send messages to myself.")


    def test_view_url_send_message_to_other(self):
        self.client.post(reverse('chat:login'),
            {'username': self.user1.username, 'password': 'pass'})

        response = self.client.post(reverse('chat:message', kwargs={'receiver_id': 2}),
                                 {'message': 'this is text'})               

        self.assertEqual(response.status_code, 201)


    def test_view_url_send_empty_message(self):
        self.client.post(reverse('chat:login'),
            {'username': self.user1.username, 'password': 'pass'})

        response = self.client.post(reverse('chat:message', kwargs={'receiver_id': 2}),
                                 {'message': ''})
        response_content_json = json.loads(response.content)

        self.assertEqual(response_content_json['message'][0], "This field may not be blank.")
