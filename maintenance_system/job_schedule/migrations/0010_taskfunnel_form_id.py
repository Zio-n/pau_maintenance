# Generated by Django 5.0.2 on 2024-05-05 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_schedule', '0009_taskfunnel_feedback_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskfunnel',
            name='form_id',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
    ]
