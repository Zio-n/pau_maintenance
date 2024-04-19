from ninja import Router, Schema
from ninja.security import django_auth
from django.shortcuts import render, get_object_or_404
from datetime import time
from django.http import JsonResponse
from .models import ShiftSchedule
from accounts.models import User


shift_router = Router()

class shiftCreateSchema(Schema):
    shift_staff_id: str
    shift_day: str
    shift_start_time: time
    shift_end_time: time
    

# Create a shift schedule
@shift_router.post("/create",auth=django_auth)
def add_shift(request, shift_data:shiftCreateSchema):
    shift_assigned_staff = get_object_or_404(User, pk=shift_data.shift_staff_id)
    ShiftSchedule.objects.create(
        assigned_staff_id=shift_assigned_staff,
        shift_day=shift_data.shift_day,
        start_time=shift_data.shift_start_time,
        end_time=shift_data.shift_end_time,
    )

    return {"message": "Shift added successfully"}

