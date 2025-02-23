import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from users.managers import CustomUserManager


class ElRahmaUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name}_{self.last_name}_{self.phone_number}'
    
    class Meta:
        verbose_name = "المستخدم"
        verbose_name_plural  = "المستخدمين" 