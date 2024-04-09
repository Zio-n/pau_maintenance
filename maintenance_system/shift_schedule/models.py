from django.db import models
from accounts.models import User
import uuid

class ShiftSchedule(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique = True)
  shift_day = models.CharField(max_length=254, choices=(
      ('Mon', 'Monday'),
      ('Tue', 'Tuesday'),
      ('Wed', 'Wednesday'),
      ('Thu', 'Thursday'),
      ('Fri', 'Friday'),
      ('Sat', 'Saturday'),
      ('Sun', 'Sunday'),
  ))
  assigned_staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
  start_time = models.TimeField()
  end_time = models.TimeField()
