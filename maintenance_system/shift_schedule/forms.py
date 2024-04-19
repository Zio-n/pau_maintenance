from django import forms
from .models import ShiftSchedule
from accounts.models import User
from django.shortcuts import render, get_object_or_404


class ShiftScheduleForm(forms.ModelForm):
    # assigned_staff_id = forms.ChoiceField(choices=[], label='Technician')
    assigned_staff_id = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False), label='Technician')
    
    # def __init__(self, *args, **kwargs):
    #     technician_choices = kwargs.pop('technician_choices', [])
    #     super().__init__(*args, **kwargs)
    #     self.fields['assigned_staff_id'].choices = technician_choices

    class Meta:
        model = ShiftSchedule
        fields = ['shift_day', 'assigned_staff_id', 'start_time', 'end_time']
        
    # def clean_assigned_staff_id(self):
    #     assigned_staff_id = self.cleaned_data['assigned_staff_id']
    #     print(f"this is the id output {assigned_staff_id}")
    #     if assigned_staff_id:
    #         assigned_staff = get_object_or_404(User, pk=assigned_staff_id)
    #         return assigned_staff
    #     else:
    #         raise forms.ValidationError("Please select a valid technician.")
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Validate start time and end time
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        return cleaned_data
