# Generated by Django 2.1.2 on 2018-11-24 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0006_auto_20181124_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='welcome_to_orthoapp',
            name='copyright',
            field=models.TextField(blank=True),
        ),
    ]
