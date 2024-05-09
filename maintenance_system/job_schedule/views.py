from django.shortcuts import render, redirect, get_object_or_404
from .forms import UpdateJobScheduleForm, UpdateTaskForm, AddJobScheduleForm, AssignStaffForm
from .models import TaskFunnel
from django.http import JsonResponse
import uuid
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import os
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .sentiment_gen import get_sentiment
from django.contrib.auth.decorators import login_required
from accounts.models import Staff


# the team leads, ass mangaer and managers view all the jobs in their dept 
# normal staffs only see jobs that have been assigned to them
@login_required
def job_schedule(request):
    if request.method == 'POST':
        if request.POST.get('action_type') == 'update_task_schedule':
            return update_task_schedule(request)
        elif request.POST.get('action_type') == 'update_job_schedule':
            return update_job_schedule(request)
        elif request.POST.get('action_type') == 'assign_staff_job_schedule':
            return assign_staff(request)
        else:
            return redirect(request.path)
        form = ShiftScheduleForm(request.POST)
    else:
        user = request.user
        user_staff = get_object_or_404(Staff, user=user)
        # Team leads, assistant managers, and managers view all jobs in their department
        if user_staff.role in ['Team Lead Mech', 'Ass Manager Mech', 'Manager Mech']:
            unassigned_jobs = TaskFunnel.objects.filter(task_dept='Mechanical', job_status='unassigned')
            assigned_inprogres_jobs = TaskFunnel.objects.filter(task_dept='Mechanical', job_status__in=['assigned', 'in progress'])
            completed_jobs = TaskFunnel.objects.filter(task_dept='Mechanical', job_status='completed')
        elif user_staff.role in ['Team Lead Elect','Manager Elect']:
            unassigned_jobs = TaskFunnel.objects.filter(task_dept='Electrical',job_status='unassigned')            
            assigned_inprogres_jobs = TaskFunnel.objects.filter(task_dept='Electrical',job_status__in=['assigned', 'in progress'])
            completed_jobs = TaskFunnel.objects.filter(task_dept='Electrical', job_status='completed')
        elif user_staff.role in ['Team Lead HVAC', 'Manager HVAC', 'Ass Manager HVAC']:
            unassigned_jobs = TaskFunnel.objects.filter(task_dept='HVAC',job_status='unassigned')            
            assigned_inprogres_jobs = TaskFunnel.objects.filter(task_dept='HVAC',job_status__in=['assigned', 'in progress'])
            completed_jobs = TaskFunnel.objects.filter(task_dept='HVAC', job_status='completed')
        # Normal staff only see jobs assigned to them
        else:
            unassigned_jobs = TaskFunnel.objects.filter(assigned_staff_id=user,job_status='unassigned')            
            assigned_inprogres_jobs = TaskFunnel.objects.filter(assigned_staff_id=user,job_status__in=['assigned', 'in progress'])
            completed_jobs = TaskFunnel.objects.filter(assigned_staff_id=user, job_status='completed')

        
        # unassigned_jobs = TaskFunnel.objects.filter(job_status='unassigned')
        # assigned_inprogres_jobs = TaskFunnel.objects.filter(job_status__in=['assigned', 'in progress'])
        # completed_jobs = TaskFunnel.objects.filter(job_status='completed')
        
        editform = UpdateJobScheduleForm()
        edittaskform = UpdateTaskForm()
        assignStaffForm = AssignStaffForm()
        
        context = {
            'unassignedjobs': unassigned_jobs,
            'assignedjobs': assigned_inprogres_jobs,
            'completedjobs': completed_jobs,
            'editform': editform,
            'edittaskform': edittaskform,
            'assignStaffForm': assignStaffForm
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
        # get the sentiment
        feedback_sentiment = get_sentiment(feedback_text)
        if feedback_text:
            task_funnel.feedback = feedback_text
            task_funnel.feedback_sentiment = feedback_sentiment
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

@login_required
def add_job_schedule(request):
    form = AddJobScheduleForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, 'Job added successfully.')
        return redirect('fault_success')  # Redirect to desired location
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")
    return redirect(request.path)  # Fallback in case of non-POST requests



@login_required
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
        'task_floor': job_schedule.task_floor,
        'task_dept': job_schedule.task_dept,
        'customer_name': job_schedule.customer_name,
        'customer_email': job_schedule.customer_email,
        'scheduled_datetime': job_schedule.scheduled_datetime,
        'priority_level': job_schedule.priority_level,
        'feedback_post_date': job_schedule.feedback_post_date,
        'feedback': job_schedule.feedback,


    }
    
    # Conditionally add image name to the data
    if job_schedule.task_fault_image:
        image_filename = job_schedule.task_fault_image.name
        job_schedule_data['task_fault_image'] = image_filename
    return JsonResponse(job_schedule_data)

@login_required
def task_schedule_detail(request):
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
        'task_floor': job_schedule.task_floor,
        'task_dept': job_schedule.task_dept,
        'customer_name': job_schedule.customer_name,
        'customer_email': job_schedule.customer_email,
        'scheduled_datetime': job_schedule.scheduled_datetime,
        'priority_level': job_schedule.priority_level,

    }
    
    # Conditionally add image name to the data
    if job_schedule.task_fault_image:
        image_filename = job_schedule.task_fault_image.name
        job_schedule_data['task_fault_image'] = image_filename
    return JsonResponse(job_schedule_data)

@login_required
def update_job_schedule(request):
    editform = UpdateJobScheduleForm(request.POST, request.FILES)
    if editform.is_valid():
        job_id = editform.cleaned_data['update_job_id']
        job_assigned_staff = editform.cleaned_data['assigned_staff_id']
        job_status = editform.cleaned_data['job_status']
        job_task_building = editform.cleaned_data['task_building']
        job_task_location = editform.cleaned_data['task_location']
        job_task_wing = editform.cleaned_data['task_wing']
        job_task_category = editform.cleaned_data['task_category']
        job_task_asset_with_fault = editform.cleaned_data['task_asset_with_fault']
        # job_task_fault_image = editform.cleaned_data['task_fault_image']
        # uploaded_image = request.FILES["task_fault_image"]
        job_task_problem = editform.cleaned_data['task_problem']
        job_task_note = editform.cleaned_data['task_note']
        job_task_floor = editform.cleaned_data['task_floor']
        job_task_dept = editform.cleaned_data['task_dept']
        job_customer_name= editform.cleaned_data['customer_name']
        job_customer_email = editform.cleaned_data['customer_email']
        job_scheduled_datetime = editform.cleaned_data['scheduled_datetime']
        job_priority_level = editform.cleaned_data['priority_level']

        


        
        try:
            job = get_object_or_404(TaskFunnel, pk=job_id)
        except TaskFunnel.DoesNotExist:
            messages.error(request, 'Job not found.')
            return redirect('job_schedule')
        
        job.assigned_staff_id = job_assigned_staff
        job.job_status = job_status
        if job_status == 'completed':
            job.completed_date = timezone.now()
        job.task_building = job_task_building
        job.task_location = job_task_location
        job.task_wing = job_task_wing
        job.task_category = job_task_category
        job.task_asset_with_fault = job_task_asset_with_fault
        job.task_problem = job_task_problem
        job.task_note = job_task_note
        job.task_floor = job_task_floor
        job.task_dept = job_task_dept
        job.customer_name = job_customer_name
        job.customer_email = job_customer_email
        job.scheduled_datetime = job_scheduled_datetime
        job.priority_level = job_priority_level
        # print(f'image is {uploaded_image}')
        # if uploaded_image:
        #     job.task_fault_image = uploaded_image
        
        
        job.save()
        
        messages.success(request, 'Job update successfully.')
        return redirect('job_schedule')  # Redirect to desired location
    else:
        for error in editform.errors:
            messages.error(request, editform.errors[error])
    return redirect(request.path)  # Fallback in case of non-POST requests


@login_required
def update_task_schedule(request):
    editform = UpdateTaskForm(request.POST, request.FILES)
    if editform.is_valid():
        job_id = editform.cleaned_data['update_task_id']
        job_task_building = editform.cleaned_data['task_building']
        job_task_location = editform.cleaned_data['task_location']
        job_task_wing = editform.cleaned_data['task_wing']
        job_task_category = editform.cleaned_data['task_category']
        job_task_asset_with_fault = editform.cleaned_data['task_asset_with_fault']
        # uploaded_image = request.FILES["task_fault_image"]
        job_task_problem = editform.cleaned_data['task_problem']
        job_task_note = editform.cleaned_data['task_note']
        job_task_floor = editform.cleaned_data['task_floor']
        job_task_dept = editform.cleaned_data['task_dept']
        job_customer_name= editform.cleaned_data['customer_name']
        job_customer_email = editform.cleaned_data['customer_email']
        job_scheduled_datetime = editform.cleaned_data['scheduled_datetime']
        job_priority_level = editform.cleaned_data['priority_level']

        


        
        try:
            job = get_object_or_404(TaskFunnel, pk=job_id)
        except TaskFunnel.DoesNotExist:
            messages.error(request, 'Job not found.')
            return redirect('job_schedule')
        
        job.task_building = job_task_building
        job.task_location = job_task_location
        job.task_wing = job_task_wing
        job.task_category = job_task_category
        job.task_asset_with_fault = job_task_asset_with_fault
        job.task_problem = job_task_problem
        job.task_note = job_task_note
        job.task_floor = job_task_floor
        job.task_dept = job_task_dept
        job.customer_name = job_customer_name
        job.customer_email = job_customer_email
        job.scheduled_datetime = job_scheduled_datetime
        job.priority_level = job_priority_level
        # print(f'image is {uploaded_image}')
        # if uploaded_image:
        #     job.task_fault_image = uploaded_image
        
        
        job.save()
        
        messages.success(request, 'Job update successfully.')
        return redirect('job_schedule')  # Redirect to desired location
    else:
        for error in editform.errors:
            messages.error(request, editform.errors[error])
    return redirect(request.path)  # Fallback in case of non-POST requests

@login_required
def assign_staff(request):
    assignform = AssignStaffForm(request.POST)  # Pre-populate job ID
    if assignform.is_valid():
      assigned_staff = assignform.cleaned_data['assigned_staff_id']
      job_id = assignform.cleaned_data['assign_job_id']
      
      job = get_object_or_404(TaskFunnel, pk=job_id) 
      
      job.assigned_staff_id = assigned_staff
      job.job_status = 'assigned'
      job.save()
      
      # Send email notification (uncomment and configure)
      assigned_staff_email = assigned_staff.email
      
      email_html_message = render_to_string('emails/assigned_email.html')

      # Send account activation email notification
      subject = 'PAU Maintenance: You have been assigned a Task'
      from_email = settings.EMAIL_HOST_USER  # Replace with your email address
      recipient_list = [assigned_staff_email]
      send_mail(subject, '',from_email, recipient_list, html_message=email_html_message)
      
      return redirect('job_schedule')   # Redirect to job schedule detail view
    else:
        for error in editform.errors:
                messages.error(request, editform.errors[error])
        return redirect(request.path)  # Fallback in case of non-POST requests

@login_required
def delete_job_schedule(request, job_id):
    if request.method == 'POST':
        try:
            job = get_object_or_404(TaskFunnel, pk=job_id)
            job.delete()
            messages.success(request, 'Job deleted successfully.')
            return redirect('job_schedule')  # Redirect to desired location
        except TaskFunnel.DoesNotExist:
            messages.error(request, 'Job not found.')
            return redirect('job_schedule')  # Or another error page
    else:
        return redirect('job_schedule')