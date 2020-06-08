from django.db import models

TAX_LT_3_DAYS = 3
TAX_GT_3_DAYS = 5
TAX_GT_5_DAYS = 7


class Book(models.Model):
    AVAILABLE = 'A'
    BORROWED = 'B'
    status_choices = [
        (AVAILABLE, 'Disponível'),
        (BORROWED, 'Emprestado')
    ]
    status = models.CharField(max_length=1, choices=status_choices, default=AVAILABLE)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    user = models.ForeignKey('Accounts.User', on_delete=models.CASCADE, null=True)
    pickup_date = models.DateField(null=True)