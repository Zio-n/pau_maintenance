from django import forms
from .models import TaskFunnel
from accounts.models import User
from django.shortcuts import render, get_object_or_404

DEPARTMENTS = [
         ('Electrical', 'Electrical'),
        ('Mechanical', 'Mechanical'),
        ('HVAC', 'HVAC'),
]

STATUS = [
        ('unassigned', 'unassigned'),
      ('assigned', 'assigned'),
      ('in progress', 'in progress'),
      ('completed', 'completed'),
]

PRIORITY = [
    ('High', 'High'),
      ('Mid', 'Mid'),
      ('Low', 'Low'),
]

class UpdateTaskForm(forms.ModelForm):
    action_type = forms.CharField(widget=forms.HiddenInput(), initial='update_task_schedule')
    task_dept = forms.ChoiceField(choices=DEPARTMENTS, required=True,)
    priority_level = forms.ChoiceField(choices=PRIORITY, required=True,)
    update_task_id = forms.CharField(widget=forms.HiddenInput())
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action_type'].widget.attrs.update({'id': 'id_edittask_action_type'})
        self.fields['update_task_id'].widget.attrs.update({'id': 'id_edittask_update_task_id'})
        self.fields['task_building'].widget.attrs.update({'id': 'id_edittask_task_building'})
        self.fields['task_location'].widget.attrs.update({'id': 'id_edittask_task_location'})
        self.fields['task_wing'].widget.attrs.update({'id': 'id_edittask_task_wing'})
        self.fields['task_category'].widget.attrs.update({'id': 'id_edittask_task_category'})
        self.fields['task_asset_with_fault'].widget.attrs.update({'id': 'id_edittask_asset_with_fault'})
        self.fields['task_problem'].widget.attrs.update({'id': 'id_edittask_task_problem'})
        self.fields['task_note'].widget.attrs.update({'id': 'id_edittask_task_note'})
        self.fields['task_fault_image'].widget.attrs.update({'id': 'id_edittask_task_fault_image'})
        self.fields['task_floor'].widget.attrs.update({'id': 'id_edittask_task_floor'})
        self.fields['task_dept'].widget.attrs.update({'id': 'id_edittask_task_dept'})
        self.fields['customer_name'].widget.attrs.update({'id': 'id_edittask_customer_name'})
        self.fields['customer_email'].widget.attrs.update({'id': 'id_edittask_customer_email'})
        self.fields['scheduled_datetime'].widget.attrs.update({'id': 'id_edittask_scheduled_datetime'})        
        self.fields['priority_level'].widget.attrs.update({'id': 'id_edittask_priority_level'})
        self.fields['feedback'].widget.attrs.update({'id': 'id_edittask_feedback'}) 
    
    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name
    
    class Meta:
        model = TaskFunnel
        fields = ['task_dept', 'task_building', 'task_location', 'task_wing', 'task_category', 'task_asset_with_fault', 'task_problem', 'task_note', 'task_fault_image', 'task_floor', 'customer_name', 'customer_email', 'scheduled_datetime', 'priority_level', 'feedback']
        widgets = {
            'task_problem': forms.Textarea(attrs={'rows':'3'}),
            'task_note': forms.Textarea(attrs={'rows':'3'})
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class UpdateJobScheduleForm(forms.ModelForm):
    action_type = forms.CharField(widget=forms.HiddenInput(), initial='update_job_schedule')
    assigned_staff_id = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False), label='Technician')
    task_dept = forms.ChoiceField(choices=DEPARTMENTS, required=True,)
    job_status = forms.ChoiceField(choices=STATUS, required=True,)
    priority_level = forms.ChoiceField(choices=PRIORITY, required=True,)
    update_job_id = forms.CharField(widget=forms.HiddenInput())
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action_type'].widget.attrs.update({'id': 'id_edit_action_type'})
        self.fields['update_job_id'].widget.attrs.update({'id': 'id_edit_update_job_id'})
        self.fields['assigned_staff_id'].widget.attrs.update({'id': 'id_edit_assigned_staff_id'})
        self.fields['job_status'].widget.attrs.update({'id': 'id_edit_job_status'})
        self.fields['task_building'].widget.attrs.update({'id': 'id_edit_task_building'})
        self.fields['task_location'].widget.attrs.update({'id': 'id_edit_task_location'})
        self.fields['task_wing'].widget.attrs.update({'id': 'id_task_wing'})
        self.fields['task_category'].widget.attrs.update({'id': 'id_edit_task_category'})
        self.fields['task_asset_with_fault'].widget.attrs.update({'id': 'id_task_asset_with_fault'})
        self.fields['task_problem'].widget.attrs.update({'id': 'id_edit_task_problem'})
        self.fields['task_note'].widget.attrs.update({'id': 'id_edit_task_note'})
        self.fields['task_fault_image'].widget.attrs.update({'id': 'id_edit_task_fault_image'})
        self.fields['task_floor'].widget.attrs.update({'id': 'id_edit_task_floor'})
        self.fields['task_dept'].widget.attrs.update({'id': 'id_edit_task_dept'})
        self.fields['customer_name'].widget.attrs.update({'id': 'id_edit_customer_name'})
        self.fields['customer_email'].widget.attrs.update({'id': 'id_edit_customer_email'})
        self.fields['scheduled_datetime'].widget.attrs.update({'id': 'id_edit_scheduled_datetime'})        
        self.fields['priority_level'].widget.attrs.update({'id': 'id_edit_priority_level'})
        self.fields['feedback'].widget.attrs.update({'id': 'id_edit_feedback'}) 
                
        self.fields['assigned_staff_id'].label_from_instance = self.label_from_instance
    
    @staticmethod
    def label_from_instance(obj):
        return "%s" % obj.name
    
    class Meta:
        model = TaskFunnel
        fields = ['assigned_staff_id', 'job_status', 'task_dept', 'task_building', 'task_location', 'task_wing', 'task_category', 'task_asset_with_fault', 'task_problem', 'task_note', 'task_fault_image', 'task_floor', 'customer_name', 'customer_email', 'scheduled_datetime', 'priority_level', 'feedback']
        widgets = {
            'task_problem': forms.Textarea(attrs={'rows':'3'}),
            'task_note': forms.Textarea(attrs={'rows':'3'})
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
