# Generated by Django 3.0.7 on 2020-06-06 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_auto_20200605_1926'),
        ('Books', '0002_book_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.User'),
        ),
    ]
