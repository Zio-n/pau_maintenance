from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    username = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
      
    
class Staff(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique = True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  ROLE_CHOICES = (
      ('Admin','Admin'),
      ('Team Lead Mech', 'Team Lead Mech'),
      ('Team Lead Elect', 'Team Lead Elect'),
      ('Team Lead HVAC', 'Team Lead HVAC'),
      ('Ass Manager Mech', 'Ass Manager Mech'),
      ('Manager Mech', 'Manager Mech'),
      ('Manager HVAC', 'Manager HVAC'),
      ('Ass Manager HVAC', 'Ass Manager HVAC'),
      ('Manager Elect', 'Manager Elect'),
      ('Elect Technician', 'Elect Technician'),
      ('Mech Technician', 'Mech Technician'),
      ('HVAC Technician', 'HVAC Technician'),
  )
  role = models.CharField(max_length=254, choices=ROLE_CHOICES)
  department = models.CharField(max_length=254, blank=True, null=True)

  
  
  def save(self, *args, **kwargs):
        department_shorthands = {
            'Elect': 'Electrical',
            'Mech': 'Mechanical',
            'HVAC': 'HVAC',
            'Admin': 'Admin',  # Add Admin department
        }

        # Check for department shorthands in role (case-insensitive)
        for shorthand, department_name in department_shorthands.items():
            if shorthand.lower() in self.role.lower():
                self.department = department_name
                break  # Exit loop after finding a match

        super().save(*args, **kwargs)

  def __str__(self):
      return self.user.name
    
    
    