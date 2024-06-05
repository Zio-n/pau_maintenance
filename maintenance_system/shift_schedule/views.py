from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, Staff
from  .forms import ShiftScheduleForm, UpdateShiftScheduleForm, GenShiftScheduleForm
from django.contrib import messages
from .models import ShiftSchedule
from django.http import JsonResponse
import os
from django.http import HttpResponse
from django.conf import settings
import csv
from datetime import datetime, timedelta
import pandas as pd

# Create your views here.
def shift_schedule(request):
    if request.method == 'POST':
        if request.POST.get('action_type') == 'add_schedule':
            return add_shift_schedule(request)
        elif request.POST.get('action_type') == 'update_schedule':
            return edit_shift_schedule(request)
        elif request.POST.get('action_type') == 'gen_schedule':
            return shift_csv_template(request)
        else:
            return redirect(request.path)
        form = ShiftScheduleForm(request.POST)
    else:
        shifts = ShiftSchedule.objects.all()
        form = ShiftScheduleForm()
        editform = UpdateShiftScheduleForm()
        genform = GenShiftScheduleForm()
        context = {
            'form': form,
            'genform': genform,
            'editform': editform,
            'shifts': shifts,
        }
        return render(request,'shift_schedule.html', context)


def shift_csv_template(request):
    genform = GenShiftScheduleForm(request.POST)
    if genform.is_valid():
        start_date = genform.cleaned_data['start_date']
        end_date = genform.cleaned_data['end_date']
        date_length = len(pd.date_range(start_date, end_date))
        
        # get all staff memebers in signed in users department
        # Get the signed-in user
        user = request.user
        
        users_dept = get_object_or_404(Staff, user=user).department
        departments = Staff.objects.filter(department=users_dept)
        
        user_names = [user.user.name for user in departments]
        
        shift_days = ['Morning', 'Afternoon', 'Evening']
        
        repetitions = 3
        date_length_repitiion = len(pd.date_range(start_date, end_date).repeat(repetitions))



        df1 = pd.DataFrame({
                'id': range(1, len(user_names)+1),
                'Staff name': user_names,
            })
            

        df2 = pd.DataFrame({
                'id': range(1, date_length_repitiion+1),
                'Date': pd.date_range(start_date, end_date).repeat(repetitions),
            })

        df3 = pd.DataFrame({
                'id': range(1, len(shift_days * date_length)+1),
                'Shift type': shift_days * date_length,
            })
        temp_df = pd.merge(df1, df2, on='id', how='outer')

        shift_df = pd.merge(temp_df, df3, on='id', how='outer')

        shift_df_mod = shift_df.drop('id',axis=1)
        
        # Create the CSV content in memory
        csv_content = shift_df_mod.to_csv(index=False)

        # Serve the CSV as a download response
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="shifts_template.csv"'
        
    
    return response
def add_shift_schedule(request):
    form = ShiftScheduleForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Shift added successfully.')
        return redirect('shift_schedule')  # Redirect to desired location
    else:
        for error in form.errors:
            messages.error(request, form.errors[error])
    return redirect(request.path)  # Fallback in case of non-POST requests

def edit_shift_schedule(request):
    editform = UpdateShiftScheduleForm(request.POST)
    if editform.is_valid():
        shift_id = editform.cleaned_data['update_shift_id']
        shift_day = editform.cleaned_data['shift_day']
        shift_assigned_staff = editform.cleaned_data['assigned_staff_id']
        shift_start_time = editform.cleaned_data['start_time']
        shift_end_time = editform.cleaned_data['end_time']
        
        try:
            shift = get_object_or_404(ShiftSchedule, pk=shift_id)
        except ShiftSchedule.DoesNotExist:
            messages.error(request, 'Shift not found.')
            return redirect('shift_schedule')
        
        shift.shift_day = shift_day
        shift.assigned_staff_id = shift_assigned_staff  # Assuming foreign key field name
        shift.start_time = shift_start_time
        shift.end_time = shift_end_time
        shift.save()
        
        messages.success(request, 'Shift update successfully.')
        return redirect('shift_schedule')  # Redirect to desired location
    else:
        for error in editform.errors:
            messages.error(request, editform.errors[error])
    return redirect(request.path)  # Fallback in case of non-POST requests

def delete_shift_schedule(request, shift_id):
    if request.method == 'POST':
        try:
            shift = get_object_or_404(ShiftSchedule, pk=shift_id)
            shift.delete()
            messages.success(request, 'Shift deleted successfully.')
            return redirect('shift_schedule')  # Redirect to desired location
        except ShiftSchedule.DoesNotExist:
            messages.error(request, 'Shift not found.')
            return redirect('shift_schedule')  # Or another error page
    else:
        return redirect('shift_schedule')

def get_shift_schedule_item(request):
    shift_schedule_id = request.GET.get('shift_schedule_id')
    shift_schedule = get_object_or_404(ShiftSchedule, pk=shift_schedule_id)
    shift_schedule_data = {
        'shift_schedule_id': shift_schedule.pk,
        'shift_day': shift_schedule.shift_day,
        'assigned_staff_id': shift_schedule.assigned_staff_id.id,
        'start_time': shift_schedule.start_time,
        'end_time': shift_schedule.end_time,
    }
    return JsonResponse(shift_schedule_data)