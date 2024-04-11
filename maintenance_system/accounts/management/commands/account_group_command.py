from django.core.management.base import BaseCommand
from accounts.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from job_schedule.models import JobSchedule, TaskFunnel
from shift_schedule.models import ShiftSchedule


class Command(BaseCommand):
    help = 'Description of my custom command'

    def handle(self, *args, **options):
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
        # Job Schedule
        content_type = ContentType.objects.get_for_model(JobSchedule)
        job_schedule_permission = Permission.objects.filter(content_type=content_type)
        # print([perm.codename for perm in job_schedule_permission])
        # shift_schedule
        content_type = ContentType.objects.get_for_model(ShiftSchedule)
        shift_schedule_permission = Permission.objects.filter(content_type=content_type)
        # print([perm.codename for perm in shift_schedule_permission])
        # task funnel
        content_type = ContentType.objects.get_for_model(TaskFunnel)
        taks_funnel_permission = Permission.objects.filter(content_type=content_type)
        # print([perm.codename for perm in taks_funnel_permission])
        # Job Schedule permission
        for perm in job_schedule_permission:
            if perm.codename == "view_jobschedule":
                mech_tech_group.permissions.add(perm)
                elect_tech_group.permissions.add(perm)
                hvac_tech_group.permissions.add(perm)
                team_lead_mech_group.permissions.add(perm)
                team_lead_elect_group.permissions.add(perm)
                team_lead_hvac_group.permissions.add(perm)        
                ass_manager_mech_group.permissions.add(perm)
                manager_mech_group.permissions.add(perm)
                manager_hvac_group.permissions.add(perm)
                ass_manager_hvac_group.permissions.add(perm)
                manager_elect_group.permissions.add(perm)
            else:
                team_lead_mech_group.permissions.add(perm)
                team_lead_elect_group.permissions.add(perm)
                team_lead_hvac_group.permissions.add(perm)        
                ass_manager_mech_group.permissions.add(perm)
                manager_mech_group.permissions.add(perm)
                manager_hvac_group.permissions.add(perm)
                ass_manager_hvac_group.permissions.add(perm)
                manager_elect_group.permissions.add(perm)
        # Shift Schedule permissions
        for perm in shift_schedule_permission:
            if perm.codename == "view_shiftschedule":
                mech_tech_group.permissions.add(perm)
                elect_tech_group.permissions.add(perm)
                hvac_tech_group.permissions.add(perm)
                team_lead_mech_group.permissions.add(perm)
                team_lead_elect_group.permissions.add(perm)
                team_lead_hvac_group.permissions.add(perm)        
                ass_manager_mech_group.permissions.add(perm)
                manager_mech_group.permissions.add(perm)
                manager_hvac_group.permissions.add(perm)
                ass_manager_hvac_group.permissions.add(perm)
                manager_elect_group.permissions.add(perm)
            else:
                team_lead_mech_group.permissions.add(perm)
                team_lead_elect_group.permissions.add(perm)
                team_lead_hvac_group.permissions.add(perm)        
                ass_manager_mech_group.permissions.add(perm)
                manager_mech_group.permissions.add(perm)
                manager_hvac_group.permissions.add(perm)
                ass_manager_hvac_group.permissions.add(perm)
                manager_elect_group.permissions.add(perm)
            
        
        # Task funnel permissions
        for perm in taks_funnel_permission:
            team_lead_mech_group.permissions.add(perm)
            team_lead_elect_group.permissions.add(perm)
            team_lead_hvac_group.permissions.add(perm)        
            ass_manager_mech_group.permissions.add(perm)
            manager_mech_group.permissions.add(perm)
            manager_hvac_group.permissions.add(perm)
            ass_manager_hvac_group.permissions.add(perm)
            manager_elect_group.permissions.add(perm)
          
        user = User.objects.get(email="zionumoh8@gmail.com")
        user.groups.add(mech_tech_group)
        
        user = get_object_or_404(User, pk=user.id)
        
        print(user.has_perm("shift_schedule.view_shiftschedule"))
        
        self.stdout.write('My custom command executed successfully')