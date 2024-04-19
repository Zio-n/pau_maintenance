from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, SignUserForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseServerError
from django.core.mail import send_mail

# Create your views here.
def manage_accounts(request):
    inactive_users = User.objects.filter(is_active=False)
    active_users = User.objects.filter(is_active=True)
    
    context = {
        'active_users': active_users,
        'inactive_users': inactive_users,
    }

    return render(request, 'manage_accounts/manage_account.html', context)

def activate_user(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)

        user.is_active = True
        user.save()

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
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    return redirect('dashboard')  # Change 'home' to your desired redirect URL
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
    return render(request,'dashboard/dashboard.html')