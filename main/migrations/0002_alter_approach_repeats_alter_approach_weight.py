# Generated by Django 5.0.6 on 2024-07-09 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approach',
            name='repeats',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='approach',
            name='weight',
            field=models.FloatField(default=0),
        ),
    ]
