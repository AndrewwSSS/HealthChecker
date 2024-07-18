# Generated by Django 5.0.6 on 2024-07-18 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_cycling_start_less_than_or_equal_now_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='cycling',
            name='end_date_grater_than_start_date',
        ),
        migrations.RemoveConstraint(
            model_name='cycling',
            name='start_less_than_or_equal_now',
        ),
        migrations.RemoveConstraint(
            model_name='jogging',
            name='end_date_grater_than_start_date',
        ),
        migrations.RemoveConstraint(
            model_name='jogging',
            name='start_less_than_or_equal_now',
        ),
        migrations.RemoveConstraint(
            model_name='powertraining',
            name='end_date_grater_than_start_date',
        ),
        migrations.RemoveConstraint(
            model_name='powertraining',
            name='start_less_than_or_equal_now',
        ),
        migrations.RemoveConstraint(
            model_name='swimming',
            name='end_date_grater_than_start_date',
        ),
        migrations.RemoveConstraint(
            model_name='swimming',
            name='start_less_than_or_equal_now',
        ),
        migrations.RemoveConstraint(
            model_name='walking',
            name='end_date_grater_than_start_date',
        ),
        migrations.RemoveConstraint(
            model_name='walking',
            name='start_less_than_or_equal_now',
        ),
        migrations.AddConstraint(
            model_name='cycling',
            constraint=models.CheckConstraint(check=models.Q(('start__lt', models.F('end'))), name='main_cycling_end_date_grater_than_start_date'),
        ),
        migrations.AddConstraint(
            model_name='jogging',
            constraint=models.CheckConstraint(check=models.Q(('start__lt', models.F('end'))), name='main_jogging_end_date_grater_than_start_date'),
        ),
        migrations.AddConstraint(
            model_name='powertraining',
            constraint=models.CheckConstraint(check=models.Q(('start__lt', models.F('end'))), name='main_powertraining_end_date_grater_than_start_date'),
        ),
        migrations.AddConstraint(
            model_name='swimming',
            constraint=models.CheckConstraint(check=models.Q(('start__lt', models.F('end'))), name='main_swimming_end_date_grater_than_start_date'),
        ),
        migrations.AddConstraint(
            model_name='walking',
            constraint=models.CheckConstraint(check=models.Q(('start__lt', models.F('end'))), name='main_walking_end_date_grater_than_start_date'),
        ),
    ]
