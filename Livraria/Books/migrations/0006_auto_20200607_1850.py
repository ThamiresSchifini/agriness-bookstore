# Generated by Django 3.0.7 on 2020-06-07 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0005_auto_20200607_0311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='dia_locacao',
            new_name='pickup_date',
        ),
    ]
