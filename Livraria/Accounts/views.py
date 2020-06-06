from django.shortcuts import render
from Livraria.Accounts.models import User
from Livraria.Accounts.serializers import UserSerializer
from rest_framework import viewsets

# Create your views here.

class AccountsViewSet(viewsets.ModelViewSet):                  # modelviewset = todos métodos http
    queryset = User.objects.all()
    serializer_class = UserSerializer