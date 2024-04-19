from django import forms
from .models import ShiftSchedule
from accounts.models import User
from django.shortcuts import render, get_object_or_404


class ShiftScheduleForm(forms.ModelForm):
    # assigned_staff_id = forms.ChoiceField(choices=[], label='Technician')
    assigned_staff_id = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False), label='Technician')
    action_type = forms.CharField(widget=forms.HiddenInput(), initial='add_schedule')

    class Meta:
        model = ShiftSchedule
        fields = ['shift_day', 'assigned_staff_id', 'start_time', 'end_time']
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Validate start time and end time
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data


class UpdateShiftScheduleForm(forms.ModelForm):
    # assigned_staff_id = forms.ChoiceField(choices=[], label='Technician')
    assigned_staff_id = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False), label='Technician')
    action_type = forms.CharField(widget=forms.HiddenInput(), initial='update_schedule')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shift_day'].widget.attrs.update({'id': 'id_edit_shift_day'})
        self.fields['assigned_staff_id'].widget.attrs.update({'id': 'id_edit_assigned_staff'})
        self.fields['start_time'].widget.attrs.update({'id': 'id_edit_start_time'})
        self.fields['end_time'].widget.attrs.update({'id': 'id_edit_end_time'})
        
    class Meta:
        model = ShiftSchedule
        fields = ['shift_day', 'assigned_staff_id', 'start_time', 'end_time']
        
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Validate start time and end time
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data
