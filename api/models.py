from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from api.managers import CustomUserManager
from django_mysql.models import JSONField


# User Role Table.
class Role(models.Model):
    Admin = 1
    Empoyee = 2

    ROLE_CHOICES = [
        (Admin, 'Admin'),
        (Empoyee, 'Empoyee'),
    ]
    role = models.CharField(
        max_length=15,
        default='Empoyee',
        null=False
    )

    class Meta:
        db_table = "user_roles"


## User Manager class.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100,unique=True,null=True, blank=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['first_name', 'last_name','email',]),
        ]

#### User search city based forecast store in data.

class UserForecastStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    search_city = models.CharField(max_length=100, null=True, blank=True)
    search_data = JSONField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_forecast_stores'
        indexes = [
            models.Index(fields=['user', 'search_city',]),
        ]
        