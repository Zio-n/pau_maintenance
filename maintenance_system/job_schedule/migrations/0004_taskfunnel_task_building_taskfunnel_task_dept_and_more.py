# Generated by Django 5.0.2 on 2024-05-04 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_schedule', '0003_alter_jobschedule_assigned_staff_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskfunnel',
            name='task_building',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='taskfunnel',
            name='task_dept',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='taskfunnel',
            name='task_problem',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
