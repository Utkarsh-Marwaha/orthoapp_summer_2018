# Generated by Django 2.1.1 on 2019-01-23 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190123_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='operationSide',
            field=models.CharField(choices=[('Left', 'Left'), ('Right', 'Right'), ('Both', 'Both')], max_length=5),
        ),
        migrations.AlterField(
            model_name='operation',
            name='operationType',
            field=models.CharField(choices=[('Knee', 'Knee'), ('Hip', 'Hip')], max_length=5),
        ),
        migrations.AlterField(
            model_name='operation',
            name='surgeryType',
            field=models.CharField(choices=[('Pri', 'Primary'), ('Rev', 'Revision')], max_length=5),
        ),
    ]
