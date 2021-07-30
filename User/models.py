from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    category_choice = (('admin', 'admin'), ('member', 'member'))  # 用户类别
    category = models.CharField(max_length=32, choices=category_choice)

    class Meta:
        db_table = 'users'
