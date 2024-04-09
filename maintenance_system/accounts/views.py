from django.shortcuts import render

# Create your views here.
def manage_accounts(request):
    return render(request, 'manage_accounts/manage_account.html')

def signup(request):
    return render(request,'signup.html')

def signin(request):
    return render(request,'signin.html')

def forgot_password(request):
    return render(request,'forgot_password.html')

def reset_password(request):
    return render(request,'reset_password.html')