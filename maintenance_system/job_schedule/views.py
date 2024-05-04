from django.shortcuts import render
from .forms import UpdateJobScheduleForm, UpdateTaskForm
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
        editform = UpdateJobScheduleForm()
        edittaskform = UpdateTaskForm()
        
        context = {
            'editform': editform,
            'edittaskform': edittaskform
        }
    return render(request,'job_schedule.html', context)

def update_task_schedule(request):
    pass

def update_job_schedule(request):
    pass