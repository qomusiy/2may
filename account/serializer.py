import hashlib

from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'password']
        model = User

