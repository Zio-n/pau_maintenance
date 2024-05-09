from django.urls import include, path
from accounts.views import manage_accounts, signup, signin, forgot_password, reset_password, signup_success, logout_view


urlpatterns = [
    path('manage/', manage_accounts, name='manage_account'),
    path('signup/', signup, name='signup'),
    path('signup_success/', signup_success, name='signup_success'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/', reset_password, name='reset_password'),
]