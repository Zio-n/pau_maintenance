from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, SignUserForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User, Staff
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseServerError
from django.core.mail import send_mail
from django.contrib.auth.models import Group, Permission
from job_schedule.models import TaskFunnel
from django.db.models import Avg, F

# Create your views here.
def manage_accounts(request):
    inactive_users = User.objects.filter(is_active=False)
    active_users = User.objects.filter(is_active=True)
    roles = ['Admin', 'Team Lead Mech', 'Team Lead Elect', 'Team Lead HVAC', 'Ass Manager Mech', 'Manager Mech', 'Manager HVAC', 'Ass Manager HVAC', 'Manager Elect', 'Elect Technician', 'Mech Technician', 'HVAC Technician']
    context = {
        'roles': roles,
        'active_users': active_users,
        'inactive_users': inactive_users,
    }

    return render(request, 'manage_accounts/manage_account.html', context)

def activate_user(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
        
        # Extract role from the request.POST dictionary
        role = request.POST.get('role')
        if role == '--------':
            messages.error(request, 'A Role is required')
            return redirect('manage_account')
        else:
            # Update the associated Staff model instance with the selected role
            staff, _ = Staff.objects.get_or_create(user=user)
            staff.role = role
            staff.save()
            
            user.is_active = True
            user.save()
            
             # give persmisions
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
             # Admin
            admin_group, created = Group.objects.get_or_create(name="Admin")
        
            if role == 'Admin':
                user.groups.add(admin_group)
            elif role == 'Team Lead Mech':
                user.groups.add(team_lead_mech_group)
            elif role == 'Team Lead Elect':
                user.groups.add(team_lead_elect_group)
            elif role == 'Team Lead HVAC':
                user.groups.add(team_lead_hvac_group)
            elif role == 'Ass Manager Mech':
                user.groups.add(ass_manager_mech_group)
            elif role == 'Manager Mech':
                user.groups.add(manager_mech_group)
            elif role == 'Manager HVAC':
                user.groups.add(manager_hvac_group)
            elif role == 'Ass Manager HVAC':
                user.groups.add(ass_manager_hvac_group)
            elif role == 'Manager Elect':
                user.groups.add(manager_elect_group)
            elif role == 'Elect Technician':
                user.groups.add(elect_tech_group)
            elif role == 'Mech Technician':
                user.groups.add(mech_tech_group)
            elif role == 'HVAC Technician':
                user.groups.add(hvac_tech_group)
            else:
                messages.error(request, 'A Role is required')
                return redirect('manage_account')

            # Render the HTML email template
            email_html_message = render_to_string('emails/confirmation_email.html')

            # Send account activation email notification
            subject = 'PAU Maintenance: Your Account Has Been Activated!'
            from_email = settings.EMAIL_HOST_USER  # Replace with your email address
            recipient_list = [user.email]
            send_mail(subject, '',from_email, recipient_list, html_message=email_html_message)

            # Redirect to success page or login page after activation
            return redirect('manage_account')  # Replace with your login URL
    except Exception as e:
        # Log the error or handle it appropriately
        return HttpResponseServerError(f"An error occurred during account activation. Please try again later. {e}")

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.is_active = False  # Set is_active to False for admin review
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('signup_success')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
            return redirect(request.path)
    else:
        form = UserForm()
    context = {
        'form': form,
        }
    return render(request,'signup.html', context)

def signup_success(request):
    return render(request,'signup_success.html')


def signin(request):
    if request.method == 'POST':
        form = SignUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # user must be active and be a registered staff with a role
                if user.is_active:
                    try:
                        staff = Staff.objects.get(user=user)
                        if staff.role:
                            # User has a role assigned, log in
                            login(request, user)
                            return redirect('dashboard')
                        else:
                            # User is not associated with a role
                            messages.error(request, 'You do not have a role assigned. Please contact an administrator.')
                            return redirect(request.path)
                    except Staff.DoesNotExist:
                        # User is not associated with a Staff model
                        messages.error(request, 'You do not have a role assigned. Please contact an administrator.')
                        return redirect(request.path)
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect(request.path)
    else:
        form = SignUserForm()
    context = {
        'form': form,
    }
    return render(request, 'signin.html', context)


def forgot_password(request):
    return render(request,'forgot_password.html')

def reset_password(request):
    return render(request,'reset_password.html')

def dashboard(request):
  completed_jobs = TaskFunnel.objects.filter(job_status='completed')
  total_jobs = completed_jobs.count()

  # Calculate average resolution time (consider edge case of no completed jobs)
  if completed_jobs.exists():
    average_resolution_time = completed_jobs.aggregate(avg_resolution_time=Avg(F('completed_date') - F('task_upload_date')))['avg_resolution_time']
  else:
    average_resolution_time = None

  context = {
    'total_jobs': total_jobs,
    'average_resolution_time': average_resolution_time,
    # Add other relevant data for the dashboard here
  }
  return render(request, 'dashboard/dashboard.html', context)