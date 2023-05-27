from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, blank=False, error_messages={
        'required': "Username must be provided.",
        'unique': "A user with that username already exists."
    })
    verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    

    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"

    def __unicode__(self):
        return self.email

    objects = UserManager()