from django.db import models
from accounts.models import User
import uuid

class ShiftSchedule(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique = True)
  shift_date = models.DateField(blank=True, null=True)
  assigned_staff_name = models.CharField(max_length=254,default='')
  shift_type = models.CharField(max_length=254, choices=(
      ('Morning', 'Morning'),
      ('Afternoon', 'Afternoon'),
      ('Evening', 'Evening'),
  ), null=True, blank=True)
  # Not used
  shift_day = models.CharField(max_length=254, choices=(
      ('Mon', 'Monday'),
      ('Tue', 'Tuesday'),
      ('Wed', 'Wednesday'),
      ('Thu', 'Thursday'),
      ('Fri', 'Friday'),
      ('Sat', 'Saturday'),
      ('Sun', 'Sunday'),
  ),null=True, blank=True)
  start_time = models.TimeField(null=True, blank=True)
  end_time = models.TimeField(null=True, blank=True)
  