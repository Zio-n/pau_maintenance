from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, SignUserForm, ForgotPasswordForm, ChngPasswordForm
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
from django.http import JsonResponse
from django.db.models import Avg, F, Count, Case, When, IntegerField, Sum, Value
import json
from django.utils.crypto import get_random_string
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def manage_accounts(request):
    user = request.user
    inactive_users = User.objects.filter(is_active=False)
    active_users = User.objects.filter(is_active=True)
    roles = ['Admin', 'Team Lead Mech', 'Team Lead Elect', 'Team Lead HVAC', 'Ass Manager Mech', 'Manager Mech', 'Manager HVAC', 'Ass Manager HVAC', 'Manager Elect', 'Elect Technician', 'Mech Technician', 'HVAC Technician']
    context = {
        'roles': roles,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'user': user
    }

    return render(request, 'manage_accounts/manage_account.html', context)

@login_required
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
    if request.method == 'POST':
        forgotForm = ForgotPasswordForm(request.POST)
        if forgotForm.is_valid():
            email = forgotForm.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate a new password
                new_password = get_random_string(length=8)  # You can specify the length you want

                # Set the new password for the user
                user.set_password(new_password)
                user.save()
                # User exists, send password reset email
                subject = 'PAU Maintenance: Password reset'
                from_email = settings.EMAIL_HOST_USER  # Replace with your email address
                recipient_list = [user.email]
                email_context ={'new_password': new_password, 'user_name': user.name}
                email_html_message = render_to_string('emails/password_reset_email.html', email_context)
                send_mail(subject, '',from_email, recipient_list, html_message=email_html_message)
                messages.success(request, 'A new password has been sent to your email address.')
                return redirect('signin')
            except User.DoesNotExist:
                messages.error(request, 'This Email Address does not exist')
                return redirect(request.path)
    else:
        forgotForm = ForgotPasswordForm()
        context = {
            'forgotForm': forgotForm,
        }
        return render(request,'forgot_password.html',context)

@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        password_form = ChngPasswordForm(user, request.POST)
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)  # Prevents user from being logged out
            messages.success(request, "Password has been changed", extra_tags='password_success')
            return redirect('dashboard')
        else:
            for error in password_form.errors:
                messages.error(request, str(password_form.errors[error][0]), extra_tags='password_error')
                return redirect(request.path)
    else:
        password_form = ChngPasswordForm(user)
        context = {
            'chngPasswordForm': password_form,
            'user': user
        }
        return render(request, 'change_password.html', context)
    
@login_required
def dashboard(request):
    postive_feedback = TaskFunnel.objects.filter(feedback_sentiment='POSITIVE').count()
    neutral_feedback = TaskFunnel.objects.filter(feedback_sentiment='NEUTRAL').count()
    negative_feedback = TaskFunnel.objects.filter(feedback_sentiment='NEGATIVE').count()    
    completed_jobs = TaskFunnel.objects.filter(job_status='completed')
    in_progress_jobs = TaskFunnel.objects.filter(job_status='in progress').count()
    assigned_jobs = TaskFunnel.objects.filter(job_status='assigned').count()
    unassigned_jobs = TaskFunnel.objects.filter(job_status='unassigned').count()
    total_jobs = completed_jobs.count()
    user = request.user
    
    top_assigned_staff = TaskFunnel.objects.filter(job_status='completed').values('assigned_staff_id').annotate(total_completed_jobs=Count('id')).order_by('-total_completed_jobs')[:5]
    # print(f'asigne {top_assigned_staff}')
    top_assigned_staff_with_users = []
    
    # Prepare job trend data
    completed_jobs_for_trend = TaskFunnel.objects.filter(job_status='completed').order_by('-completed_date')[:7]  # Get recent completed jobs (modify limit as needed)
    job_trend_data = []
    job_trend_labels = []
    for job in completed_jobs_for_trend:
        job_trend_data.append(completed_jobs.count())  # Assuming a count field exists in the model (replace with your field name)
        job_trend_labels.append(job.completed_date.strftime('%d %b %Y'))  # Format date for labels
    
    for staff in top_assigned_staff:
        user = get_object_or_404(User, pk=staff['assigned_staff_id'])
        top_assigned_staff_with_users.append({
                'user': user.name,
                'total_completed_jobs': staff['total_completed_jobs']
            })
    top_staffs = json.dumps(top_assigned_staff_with_users)
    job_trend_data_populate = json.dumps(job_trend_data)
    job_trend_labels_populate = json.dumps(job_trend_labels)
    job_status ={
        'unassigned': unassigned_jobs,
        'assigned': assigned_jobs,
        'in_progress': in_progress_jobs,
        'completed': total_jobs,
    }
    feedback_sentiment = {
        'positive': postive_feedback,
        'neutral': neutral_feedback,
        'negative': negative_feedback,
    }
    
    # Average customers satisfaction score
    sentiment_values = {
        'POSITIVE': 100,
        'NEUTRAL': 50,
        'NEGATIVE': 0
    }

    # Calculate the sum of sentiment scores and the total number of feedback
    satisfaction_data = TaskFunnel.objects.annotate(
        sentiment_score=Case(
            *[When(feedback_sentiment=sentiment, then=Value(score)) for sentiment, score in sentiment_values.items()],
            default=Value(0),
            output_field=IntegerField()
        )
    ).aggregate(
        total_feedback=Count('id'),
        total_score=Sum('sentiment_score')
    )
    print(satisfaction_data['total_feedback'])
    # Calculate the average satisfaction score
    if satisfaction_data['total_feedback'] > 0:
        average_satisfaction_score = (satisfaction_data['total_score'] / satisfaction_data['total_feedback'])
    else:
        average_satisfaction_score = 0
    
    
    # Calculate average resolution time (consider edge case of no completed jobs)
    if completed_jobs.exists():
        average_resolution_time = completed_jobs.aggregate(avg_resolution_time=Avg(F('completed_date') - F('task_upload_date')))['avg_resolution_time']
    else:
        average_resolution_time = None

    context = {
        'total_jobs': total_jobs,
        'average_resolution_time': average_resolution_time,
        'job_status': job_status,
        'top_staffs': top_staffs,
        'job_trend_data': job_trend_data_populate,
        'job_trend_labels': job_trend_labels_populate,
        'feedback_sentiment': feedback_sentiment,
        'average_satisfaction_score': average_satisfaction_score,
        'user': user
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def logout_view(request):
    logout(request)