# Generated by Django 5.0.2 on 2024-05-04 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_schedule', '0008_taskfunnel_task_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskfunnel',
            name='feedback_post_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
