# Generated by Django 2.1.5 on 2019-01-25 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('0', 'Female'), ('1', 'Male')], max_length=15, null=True),
        ),
    ]
