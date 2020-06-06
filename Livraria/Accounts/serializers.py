from rest_framework import serializers
from Livraria.Accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'schooling', 'id']
