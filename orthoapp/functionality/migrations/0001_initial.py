# Generated by Django 2.1.5 on 2019-01-23 12:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=512)),
                ('time', models.DateTimeField()),
                ('time_zone', timezone_field.fields.TimeZoneField(default='Australia/Sydney')),
                ('task_id', models.CharField(blank=True, editable=False, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='KneeMotionRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bend', models.FloatField(default=90)),
                ('stretch', models.FloatField(default=90)),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Operation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PainLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('painLevel', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('isExerciseDone', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('isMedicineTaken', models.BooleanField()),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Operation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StepCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('steps', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Operation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
