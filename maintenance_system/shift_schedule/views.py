from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, Staff
from  .forms import ShiftScheduleForm, UpdateShiftScheduleForm, GenShiftScheduleForm, UploadCSVForm
from django.contrib import messages
from .models import ShiftSchedule
from django.http import JsonResponse
import os
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
import csv
from datetime import datetime, timedelta
import pandas as pd
import io
import magic


# Create your views here.
def shift_schedule(request):
    if request.method == 'POST':
        if request.POST.get('action_type') == 'add_schedule':
            return add_shift_schedule(request)
        elif request.POST.get('action_type') == 'update_schedule':
            return edit_shift_schedule(request)
        elif request.POST.get('action_type') == 'gen_schedule':
            return shift_csv_template(request)
        elif request.POST.get('action_type') == 'upload_schedule':
            return upload_shift(request)
        else:
            return redirect(request.path)
        form = ShiftScheduleForm(request.POST)
    else:
        shifts = ShiftSchedule.objects.all()
        form = ShiftScheduleForm()
        editform = UpdateShiftScheduleForm()
        genform = GenShiftScheduleForm()
        uploadform = UploadCSVForm()
        context = {
            'form': form,
            'genform': genform,
            'editform': editform,
            'uploadform': uploadform,
            'shifts': shifts,
        }
        return render(request,'shift_schedule.html', context)


# Generate shift template
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


# Uploa shift template
def upload_shift(request):
    uploadform = UploadCSVForm(request.POST, request.FILES)
    if uploadform.is_valid():
        csv_file = request.FILES['csv_file']
        user = request.user
        users_dept = get_object_or_404(Staff, user=user).department
        # Use python-magic to check the MIME type
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_buffer(csv_file.read(1024))
        csv_file.seek(0)  # Reset the file pointer to the beginning

        valid_mime_types = ['text/csv', 'application/csv', 'text/plain', 'application/vnd.ms-excel']
        if file_mime_type not in valid_mime_types or not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return redirect(request.path)
        

        # Use pandas to read the CSV file
        try:
            data_set = pd.read_csv(csv_file).fillna('')
        except pd.errors.ParserError:
            messages.error(request, 'Error reading CSV file. Please check the file format.')
            return redirect(request.path)

        # Check if all required columns are present
        required_columns = ['Staff name', 'Date', 'Shift type']
        if not all(column in data_set.columns for column in required_columns):
            messages.error(request, 'CSV file is missing required columns.')
            return redirect(request.path)
        
        
        num_shifts_added = 0
        with transaction.atomic():
            # Iterate through the DataFrame rows
            for index, row in data_set.iterrows():
                staff_name = row.get('Staff name', '').strip()
                shift_date = row.get('Date', '').strip()
                shift_type = row.get('Shift type', '').strip()

                if not staff_name or not shift_type:
                    continue  # Skip rows where both 'Staff name' and 'Shift type' are empty

                try:
                    shift_date = datetime.strptime(shift_date, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request, f'Invalid date format in row {index+2}.')
                    return redirect(request.path)

                shift_day = shift_date.strftime('%a')  # Get the abbreviated day of the week (Mon, Tue, etc.)

                ShiftSchedule.objects.create(
                    assigned_staff_name=staff_name,
                    shift_date=shift_date,
                    shift_day=shift_day,
                    shift_dept=users_dept,
                    shift_type=shift_type
                )
                num_shifts_added += 1
            
            messages.success(request, f'Successfully added {num_shifts_added} shifts.')
            return redirect(request.path)

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