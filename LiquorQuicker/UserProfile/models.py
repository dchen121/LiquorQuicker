from django.db import models
from django.contrib.auth.models import AbstractUser


class LQUser(AbstractUser):
    """
    A custom User model which includes a avatar field for a user image
    """
    avatar = models.ImageField('photos/%Y/%m/%d')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
