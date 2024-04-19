from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from  .forms import ShiftScheduleForm, UpdateShiftScheduleForm
from django.contrib import messages
from .models import ShiftSchedule
from django.http import JsonResponse


# Create your views here.
def shift_schedule(request):
    if request.method == 'POST':
        if request.POST.get('action_type') == 'add_schedule':
            return add_shift_schedule(request)
        elif request.POST.get('action_type') == 'update_schedule':
            return edit_shift_schedule(request)
        else:
            return redirect(request.path)
        form = ShiftScheduleForm(request.POST)
    else:
        shifts = ShiftSchedule.objects.all()
        form = ShiftScheduleForm()
        editform = UpdateShiftScheduleForm()
        context = {
            'form': form,
            'editform': editform,
            'shifts': shifts,
        }
        return render(request,'shift_schedule.html', context)



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