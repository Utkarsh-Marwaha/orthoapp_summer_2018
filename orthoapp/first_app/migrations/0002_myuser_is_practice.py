# Generated by Django 2.1.2 on 2018-12-04 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_practice',
            field=models.BooleanField(default=True, verbose_name='surgeon status'),
        ),
    ]