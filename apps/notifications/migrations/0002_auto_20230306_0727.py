# Generated by Django 3.2.18 on 2023-03-06 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payload',
            name='body',
            field=models.CharField(default=None, max_length=120),
        ),
        migrations.AlterField(
            model_name='payload',
            name='title',
            field=models.CharField(default=None, max_length=30),
        ),
    ]