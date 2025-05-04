from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE())
    title = models.CharField(max_length=150)
    desc = models.TextField()
    price = models.DecimalField(10, 2)
