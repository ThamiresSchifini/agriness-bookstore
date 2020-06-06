from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    schooling = models.CharField(max_length=50)
    id = models.CharField(primary_key=True, max_length=20)

