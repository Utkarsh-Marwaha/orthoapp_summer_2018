# Generated by Django 2.1.5 on 2019-01-23 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('developer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information_Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('main_text', models.TextField(blank=True)),
                ('surgery_stage', models.CharField(choices=[('PRE', 'Pre Surgery'), ('PST', 'Post Surgery')], max_length=10)),
                ('hospital_name', models.CharField(choices=[('OA', 'Orthopaedics ACT'), ('CL', 'Calvary')], max_length=20)),
                ('photo_main', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('photo_1', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_2', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_3', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('photo_4', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('is_key_link', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='developer.Developer')),
            ],
        ),
    ]
