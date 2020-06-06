from django.db import models

# Create your models here.

class book(models.Model):
    AVAILABLE = 'A'
    BORROWED = 'B'
    status_choices = [
        (AVAILABLE, 'Disponível'),
        (BORROWED, 'Emprestado')
    ]
    status = models.CharField(max_length=1, choices=status_choices, default=AVAILABLE)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    user = models.ForeignKey('Accounts.User', on_delete=models.CASCADE)