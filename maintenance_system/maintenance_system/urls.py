"""
URL configuration for maintenance_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from accounts.views import dashboard, activate_user
from shift_schedule.views import shift_schedule, get_shift_schedule_item, delete_shift_schedule, shift_csv_template
from job_schedule.views import job_schedule, send_feedback_email, show_image, job_schedule_detail, task_schedule_detail, delete_job_schedule, fault_form, fault_success, feedback_form, feedback_success
from maintenance_system.api import api as maintenance_system_api
urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('user/', include("accounts.urls")),
    path('shifts/', shift_schedule, name="shift_schedule"),
    path("shift_template/", shift_csv_template, name="shift_template"),
    path('jobs/', job_schedule, name="job_schedule"),
    path('shift_detail/', get_shift_schedule_item, name="shift_detail"),
    path('job_detail/', job_schedule_detail, name="job_detail"),
    path('task_detail/', task_schedule_detail, name="task_detail"),
    # forms
    path('fault_form/', fault_form, name="fault_form"),
    path('fault_success/', fault_success, name="fault_success"),
    path('feedback_success/', feedback_success, name="feedback_success"),
    path('shift_delete/<uuid:shift_id>/', delete_shift_schedule, name="delete_shift"),
    path('job_delete/<uuid:job_id>/', delete_job_schedule, name="delete_job"),
    path('send_feedback_email/<uuid:job_id>/', send_feedback_email, name="send_feedback_email"),
    path('feedback/', feedback_form, name="feedback_form"),
    path('activate_account/<int:user_id>/', activate_user, name="activate_account"),
    path('show_image/<uuid:task_id>/', show_image, name='show_image'),
    path('dashboard/', dashboard, name='dashboard'),
    path("api/", maintenance_system_api.urls),
]
