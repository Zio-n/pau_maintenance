# Generated by Django 5.0.2 on 2024-05-08 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_schedule', '0012_alter_taskfunnel_priority_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskfunnel',
            name='completed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taskfunnel',
            name='task_upload_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
