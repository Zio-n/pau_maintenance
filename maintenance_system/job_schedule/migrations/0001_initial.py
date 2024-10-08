# Generated by Django 5.0.2 on 2024-04-09 09:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskFunnel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('task_location', models.CharField(max_length=254)),
                ('task_wing', models.CharField(max_length=254)),
                ('task_category', models.CharField(max_length=254)),
                ('task_asset_with_fault', models.CharField(max_length=254)),
                ('task_note', models.CharField(blank=True, max_length=254)),
                ('task_fault_image', models.FileField(blank=True, upload_to='fault_images/')),
                ('task_floor', models.CharField(max_length=254)),
                ('task_type', models.CharField(choices=[('Electrical', 'Electrical'), ('Mechanical', 'Mechanical'), ('HVAC', 'HVAC')], max_length=54)),
                ('customer_name', models.CharField(max_length=254)),
                ('customer_email', models.EmailField(max_length=255)),
                ('scheduled_datetime', models.DateTimeField(blank=True, null=True)),
                ('priority_level', models.CharField(blank=True, choices=[('High', 'High'), ('Mid', 'Mid'), ('Low', 'Low')], max_length=54, null=True)),
            ],
        ),
    ]
