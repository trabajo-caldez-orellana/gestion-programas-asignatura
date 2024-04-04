# serializers.py

from rest_framework import serializers
from backend.models import Usuario

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']