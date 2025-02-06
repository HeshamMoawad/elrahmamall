import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import CustomUserManager


class ElRahmaUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}_{self.phone_number}'