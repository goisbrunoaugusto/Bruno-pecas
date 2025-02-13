from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser) :
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        REGULAR = 'REGULAR', 'Regular User'

    username = models.CharField(max_length=155, unique=True)
    email = models.EmailField(max_length=155, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.REGULAR)

    first_name = None
    last_name = None

    REQUIRED_FIELDS = ['email']

    def is_admin(self):
        return self.role == self.Role.ADMIN
