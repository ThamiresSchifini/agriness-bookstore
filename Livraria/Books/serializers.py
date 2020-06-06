from rest_framework import serializers
from Livraria.Books.models import book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = book
        fields = ['status', 'name', 'author']

        # posso criar uma def aqui e alterar coisas do modelo (excluir, editar, lógica etc)