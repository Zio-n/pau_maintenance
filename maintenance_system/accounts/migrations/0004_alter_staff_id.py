# Generated by Django 5.0.2 on 2024-04-09 09:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_staff_staff_id_alter_staff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
