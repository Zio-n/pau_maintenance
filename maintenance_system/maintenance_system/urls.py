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
from accounts.views import dashboard
from shift_schedule.views import shift_schedule, get_shift_schedule_item
from maintenance_system.api import api as maintenance_system_api
urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('user/', include("accounts.urls")),
    path('shifts/', shift_schedule, name="shift_schedule"),
    path('shift_detail/', get_shift_schedule_item, name="shift_detail"),
    path('dashboard/', dashboard, name='dashboard'),
    path("api/", maintenance_system_api.urls),
]
