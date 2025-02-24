from django.db import models
from django.contrib.auth.models import AbstractUser


optional_field = {'blank': True, 'null': True}


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, **optional_field)
    first_name = models.CharField(max_length=30, **optional_field)
    last_name = models.CharField(max_length=30, **optional_field)
    profile_picture = models.ImageField(
        upload_to='profile_picture/', **optional_field)

    def __str__(self):
        return self.username
