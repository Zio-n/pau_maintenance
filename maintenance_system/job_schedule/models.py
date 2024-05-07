from django.db import models
from accounts.models import User
import uuid

# class JobSchedule(models.Model):
#   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique = True)
#   task_id = models.ForeignKey('TaskFunnel', on_delete=models.CASCADE)
#   assigned_staff_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#   job_status = models.CharField(max_length=100, choices=(
#       ('unassigned', 'unassigned'),
#       ('assigned', 'assigned'),
#       ('in progress', 'in progress'),
#       ('completed', 'completed'),
#   ))
#   feedback = models.TextField(blank=True)

class TaskFunnel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique = True)
    task_num = models.PositiveIntegerField(unique=True, blank=True, null=True)
    assigned_staff_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    job_status = models.CharField(max_length=100, choices=(
        ('unassigned', 'unassigned'),
        ('assigned', 'assigned'),
        ('in progress', 'in progress'),
        ('completed', 'completed'),
    ), default='unassigned')
    task_building = models.CharField(max_length=254, blank=True)
    task_location = models.CharField(max_length=254)
    task_wing = models.CharField(max_length=254)
    task_category = models.CharField(max_length=254)
    task_asset_with_fault = models.CharField(max_length=254)
    task_problem = models.CharField(max_length=254, blank=True)
    task_note = models.CharField(max_length=254, blank=True)
    task_fault_image = models.FileField(upload_to='fault_images/', blank=True)
    task_floor = models.CharField(max_length=254)
    task_dept = models.CharField(max_length=54, choices=(
        ('Electrical', 'Electrical'),
        ('Mechanical', 'Mechanical'),
        ('HVAC', 'HVAC'),
    ))
    form_id = models.UUIDField(editable=False, unique = True, blank=True, null=True)
    customer_name = models.CharField(max_length=254)
    customer_email = models.EmailField(max_length=255)
    scheduled_datetime = models.DateField(blank=True, null=True)
    priority_level = models.CharField(max_length=54, blank=True, null=True, choices=(
        ('High', 'High'),
        ('Mid', 'Mid'),
        ('Low', 'Low'),
    ), default='Mid')
    feedback_post_date = models.DateField(blank=True, null=True)
    feedback_url_status = models.BooleanField(default=True)
    feedback = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.task_num:
            # Get the maximum task_num value and increment by 1
            last_task = TaskFunnel.objects.order_by('-task_num').first()
            self.task_num = last_task.task_num + 1 if last_task else 1
        super().save(*args, **kwargs)