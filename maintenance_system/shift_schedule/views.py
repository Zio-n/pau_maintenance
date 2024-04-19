from django.shortcuts import render, redirect
from accounts.models import User
from  .forms import ShiftScheduleForm
from django.contrib import messages

# Create your views here.
def shift_schedule(request):
    if request.method == 'POST':
        form = ShiftScheduleForm(request.POST)
        print('form stopped')
        # assigned_selected = request.POST.get('assigned_staff_id')

        # form.fields['assigned_staff_id'].choices = [(assigned_selected, assigned_selected)]
        if form.is_valid():
            print('form is valid')
            form.save()
            messages.success(request, 'Shift added successfully.')
            return redirect('shift_schedule')
        else:
            print('form is invalid')
            for error in form.errors:
                print(f'the error is {form.errors[error]}')
                messages.error(request, form.errors[error])
    else:
        # active_users = User.objects.filter(is_active=True, is_superuser=False)
        # choices = [("", "---------")]  # Adding the default option
        # choices.extend([(user.pk, user.name) for user in active_users])
        form = ShiftScheduleForm()
        # form.fields['assigned_staff_id'].choices = choices
        context = {
            'form': form
        }
        return render(request,'shift_schedule.html', context)

def add_shift(request):
    if request.method == 'POST':
        form = ShiftScheduleForm(request.POST)
        print('form stopped')
        if form.is_valid():
            print('form is valid')
            form.save()
            messages.success(request, 'Shift added successfully.')
            return redirect('shift_schedule') 
    else:
        print('form is invalid')
        messages.error(request, 'Invalid form submission.')
    return redirect('shift_schedule') 