# Generated by Django 5.0.6 on 2024-07-07 11:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_sex'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='FoodCategory',
        ),
        migrations.RemoveField(
            model_name='swimmingtraining',
            name='duration',
        ),
        migrations.AddField(
            model_name='cyclingtraining',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='powertraining',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='swimmingtraining',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='cyclingtraining',
            name='start',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='powertraining',
            name='start',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='swimmingtraining',
            name='start',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Jogging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(auto_now_add=True)),
                ('end', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('average_speed', models.FloatField()),
                ('distance', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Walk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(auto_now_add=True)),
                ('end', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('average_speed', models.FloatField()),
                ('distance', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
