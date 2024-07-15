from django.urls import include, path
from accounts.views import manage_accounts, signup, signin, forgot_password, signup_success, change_password, logout_view
from django.contrib.auth import views as auth_views
from maintenance_system import settings

urlpatterns = [
    path('manage/', manage_accounts, name='manage_account'),
    path('signup/', signup, name='signup'),
    path('signup_success/', signup_success, name='signup_success'),
    path('signin/', signin, name='signin'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('change_password/', change_password, name='change_password'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]