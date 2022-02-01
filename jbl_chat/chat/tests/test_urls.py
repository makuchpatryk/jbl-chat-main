from django.test import TestCase
from django.urls import reverse, resolve

from chat import views

class UrlTestCase(TestCase):
    
    def test_api_url_login(self):
        url = reverse('chat:login')
        self.assertEquals(resolve(url).func.view_class, views.Login)

    def test_api_url_logout(self):
        url = reverse('chat:logout')
        self.assertEquals(resolve(url).func.view_class, views.Logout)

    def test_api_url_users(self):
        url = reverse('chat:users')
        self.assertEquals(resolve(url).func.view_class, views.Users)

    def test_api_url_message(self):
        url = reverse('chat:message', args=[1])
        self.assertEquals(resolve(url).func.view_class, views.Message)