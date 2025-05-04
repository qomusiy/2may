from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class ProductTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token )

        self.product_data = {
            'user':self.user,
            'title':'POCO X11',
            'desc': '1 tr',
            'price': 43000
        }

        self.create_product = reverse("create_product")
        self.client.post(self.create_product, self.product_data)


    def test_create(self):
        self.client.credentials(HTTP_AUTHORIZATION = "Bearer" +" "+ self.access_token)
        response = self.client.post(self.create_product, self.product_data)

        self.assertEqual(response.data['title'], 'POCO X11')


