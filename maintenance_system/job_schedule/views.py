from django.shortcuts import render
from .forms import UpdateJobScheduleForm, UpdateTaskForm
from .models import TaskFunnel
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

def update_task_schedule(request):
    pass

def update_job_schedule(request):
    pass