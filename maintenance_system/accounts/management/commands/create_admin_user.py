from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User, Staff  # Adjust the import according to your app name

class Command(BaseCommand):
    help = 'Create an admin user'

    def handle(self, *args, **kwargs):
        email = 'admin@default.com'
        password = 'admin_password'
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
        else:
            user = User.objects.create_user(
                email=email,
                password=password
            )
            Staff.objects.create(
                user=user,
                role='Admin',
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin user.'))
