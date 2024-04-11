from django.shortcuts import render, redirect
from .forms import UserForm, SignUserForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login


# Create your views here.
def manage_accounts(request):
    return render(request, 'manage_accounts/manage_account.html')


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