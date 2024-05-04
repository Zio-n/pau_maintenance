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
from shift_schedule.views import shift_schedule, get_shift_schedule_item, delete_shift_schedule
from job_schedule.views import job_schedule, job_schedule_detail
from maintenance_system.api import api as maintenance_system_api
urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('user/', include("accounts.urls")),
    path('shifts/', shift_schedule, name="shift_schedule"),
    path('jobs/', job_schedule, name="job_schedule"),
    path('shift_detail/', get_shift_schedule_item, name="shift_detail"),
    path('job_detail/', job_schedule_detail, name="job_detail"),
    path('shift_delete/<uuid:shift_id>/', delete_shift_schedule, name="delete_shift"),
    path('activate_account/<int:user_id>/', activate_user, name="activate_account"),
    path('dashboard/', dashboard, name='dashboard'),
    path("api/", maintenance_system_api.urls),
]
