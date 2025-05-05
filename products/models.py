from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'products'