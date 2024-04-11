from django.shortcuts import render

# Create your views here.
def shift_schedule(request):
    return render(request,'shift_schedule.html')