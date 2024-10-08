# Generated by Django 5.0.2 on 2024-05-04 09:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_schedule', '0004_taskfunnel_task_building_taskfunnel_task_dept_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='taskfunnel',
            name='assigned_staff_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='taskfunnel',
            name='feedback',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='taskfunnel',
            name='job_status',
            field=models.CharField(choices=[('unassigned', 'unassigned'), ('assigned', 'assigned'), ('in progress', 'in progress'), ('completed', 'completed')], default='unassigned', max_length=100),
        ),
        migrations.DeleteModel(
            name='JobSchedule',
        ),
    ]
