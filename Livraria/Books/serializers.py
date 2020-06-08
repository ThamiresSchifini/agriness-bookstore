from rest_framework import serializers

from Livraria.Books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['status', 'name', 'author']

    def get_status(self, obj):
        return 'Disponível' if obj.status == 'A' else 'Emprestado'