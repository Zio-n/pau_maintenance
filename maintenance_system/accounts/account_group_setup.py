from .models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from job_schedule.models import JobSchedule, TaskFunnel
from shift_schedule.models import ShiftSchedule

# Workers
mech_tech_group, created = Group.objects.get_or_create(name="Mech technician")
elect_tech_group, created = Group.objects.get_or_create(name="Elect technician")
hvac_tech_group, created = Group.objects.get_or_create(name="HVAC technician")
# Team leads
team_lead_mech_group, created = Group.objects.get_or_create(name="Team Lead Mech")
team_lead_elect_group, created = Group.objects.get_or_create(name="Team Lead Elect")
team_lead_hvac_group, created = Group.objects.get_or_create(name="Team Lead HVAC")
# Managers
ass_manager_mech_group, created = Group.objects.get_or_create(name="Ass Manager Mech")
manager_mech_group, created = Group.objects.get_or_create(name="Manager Mech")
manager_hvac_group, created = Group.objects.get_or_create(name="Manager HVAC")
ass_manager_hvac_group, created = Group.objects.get_or_create(name="Ass Manager HVAC")
manager_elect_group, created = Group.objects.get_or_create(name="Manager Elect")

content_type = ContentType.objects.get_for_model(JobSchedule)
job_schedule_permission = Permission.objects.filter(content_type=content_type)
print([perm.codename for perm in post_permission])