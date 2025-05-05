from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product
from .serializer import ProductSerializer
from decimal import Decimal

class ProductTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.product_data = {
            'title': 'POCO X11',
            'desc': 'Test Description',
            'price': '43000.00'
        }

        self.create_product = reverse('product-create')
        self.list_product = reverse('product-list')
        self.detail_product = lambda pk: reverse('product-detail', kwargs={'pk': pk})
        self.update_product = lambda pk: reverse('product-update', kwargs={'pk': pk})
        self.delete_product = lambda pk: reverse('product-delete', kwargs={'pk': pk})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.product = Product.objects.create(
            user=self.user,
            title='Existing Product',
            desc='Existing Description',
            price=Decimal('49999.99')
        )

    def test_serializer_valid_data(self):
        serializer = ProductSerializer(data=self.product_data, context={'request': type('Request', (), {'user': self.user})()})
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.title, 'POCO X11')
        self.assertEqual(product.desc, 'Test Description')
        self.assertEqual(product.price, Decimal('43000.00'))
        self.assertEqual(product.user, self.user)

    def test_serializer_invalid_price(self):
        invalid_data = self.product_data.copy()
        invalid_data['price'] = 'invalid'
        serializer = ProductSerializer(data=invalid_data, context={'request': type('Request', (), {'user': self.user})()})
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.create_product, self.product_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'POCO X11')
        self.assertEqual(Decimal(response.data['price']), Decimal('43000.00'))
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.last().user, self.user)

    def test_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.list_product)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Existing Product')
        self.assertEqual(Decimal(response.data[0]['price']), Decimal('49999.99'))

    def test_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.detail_product(self.product.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Existing Product')
        self.assertEqual(Decimal(response.data['price']), Decimal('49999.99'))

    def test_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        update_data = {
            'title': 'Updated Product',
            'desc': 'Updated Description',
            'price': '79999.99'
        }
        response = self.client.put(self.update_product(self.product.id), update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Product')
        self.assertEqual(Decimal(response.data['price']), Decimal('79999.99'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'Updated Product')

    def test_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.delete(self.delete_product(self.product.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_unauthenticated_access(self):
        self.client.credentials()
        response = self.client.get(self.list_product)
        self.assertEqual(response.status_code, 401)