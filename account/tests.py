from http.client import HTTPResponse

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.test_url = reverse('test')

        self.user_data = {
            'username': 'user',
            'password': 'user',
        }

        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, self.user_data)
        self.refresh_token = response.data['refresh']
        self.access_token = response.data['access']

    def test_regis(self):
        data = {
            'username': 'Humoyun',
            'password': 'admin'
        }

        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data'], 'Humoyun')

    def test_login(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, 200)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION = "Bearer" +" "+ self.access_token)
        response = self.client.post(self.logout_url, {'refresh':self.refresh_token})
        self.assertEqual(response.data['msg'], 'done')
        self.assertEqual(response.status_code, 200)

    def test_test_notreally(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('msg', response.data)

    def test_test(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer"+" "+self.access_token)
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)








