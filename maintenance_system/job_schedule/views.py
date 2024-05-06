from django.shortcuts import render, redirect, get_object_or_404
from .forms import UpdateJobScheduleForm, UpdateTaskForm, AddJobScheduleForm
from .models import TaskFunnel
from django.http import JsonResponse
import uuid
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def job_schedule(request):
    if request.method == 'POST':
        if request.POST.get('action_type') == 'update_task_schedule':
            return update_task_schedule(request)
        elif request.POST.get('action_type') == 'update_job_schedule':
            return update_job_schedule(request)
        else:
            return redirect(request.path)
        form = ShiftScheduleForm(request.POST)
    else:
        unassigned_jobs = TaskFunnel.objects.filter(job_status='unassigned')
        assigned_inprogres_jobs = TaskFunnel.objects.filter(job_status__in=['assigned', 'in progress'])
        completed_jobs = TaskFunnel.objects.filter(job_status='completed')
        
        editform = UpdateJobScheduleForm()
        edittaskform = UpdateTaskForm()
        
        context = {
            'unassignedjobs': unassigned_jobs,
            'assignedjobs': assigned_inprogres_jobs,
            'completedjobs': completed_jobs,
            'editform': editform,
            'edittaskform': edittaskform
        }
    return render(request,'job_schedule.html', context)

def fault_form(request):
    if request.method == 'POST':
          if request.POST.get('action_type') == 'add_job_schedule':
            return add_job_schedule(request)
    else:
        addform = AddJobScheduleForm()
        context={
            'addform': addform,
        }
        return render(request,'customer_forms/fault_form.html', context)
    
def fault_success(request):
    return render(request,'customer_forms/fault_form_success.html')

def feedback_success(request):
     return render(request,'customer_forms/feedback_success.html')


@csrf_exempt
def feedback_form(request):
    form_id  = request.GET.get('form_id')
    task_funnel = get_object_or_404(TaskFunnel, form_id=form_id)
    feedback_status = task_funnel.feedback_url_status
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback_text')  # Assuming feedback text is sent in the request
        if feedback_text:
            task_funnel.feedback = feedback_text
            task_funnel.feedback_post_date = timezone.now()
            task_funnel.feedback_url_status = False
            task_funnel.save()
            return redirect('feedback_success')  # Return JSON response indicating success
        else:
            return redirect(request.path)
    elif feedback_status:
        return render(request,'customer_forms/feedback.html')  # Method not allowed if request method is not POST
    else:
        return render(request,'customer_forms/feedback_inactive.html')

def add_job_schedule(request):
    form = AddJobScheduleForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Job added successfully.')
        return redirect('fault_success')  # Redirect to desired location
    else:
        for error in form.errors:
            messages.error(request, form.errors[error])
    return redirect(request.path)  # Fallback in case of non-POST requests


def job_schedule_detail(request):
    job_schedule_id = request.GET.get('job_id')
    job_schedule = get_object_or_404(TaskFunnel, id=job_schedule_id)
    assigned_name = job_schedule.assigned_staff_id.name if job_schedule.assigned_staff_id else None
    job_schedule_data = {
        'job_schedule_id': job_schedule.pk,
        'task_num': job_schedule.task_num,
        'assigned_name': assigned_name,
        'job_status': job_schedule.job_status,
        'task_building': job_schedule.task_building,
        'task_location': job_schedule.task_location,
        'task_wing': job_schedule.task_wing,
        'task_category': job_schedule.task_category,
        'task_asset_with_fault': job_schedule.task_asset_with_fault,
        'task_problem': job_schedule.task_problem,
        'task_note': job_schedule.task_note,
        # 'task_fault_image': job_schedule.task_fault_image,
        'task_floor': job_schedule.task_floor,
        'task_dept': job_schedule.task_dept,
        'customer_name': job_schedule.customer_name,
        'customer_email': job_schedule.customer_email,
        'scheduled_datetime': job_schedule.scheduled_datetime,
        'priority_level': job_schedule.priority_level,
        'feedback_post_date': job_schedule.feedback_post_date,
        'feedback': job_schedule.feedback,


    }
    return JsonResponse(job_schedule_data)

def update_task_schedule(request):
    pass

def update_job_schedule(request):
    pass