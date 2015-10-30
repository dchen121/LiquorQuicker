from django.db import models
from django.contrib.auth.models import AbstractUser


class LQUser(AbstractUser):
    """
    A custom User model which includes a avatar field for a user image
    """
    avatar = models.ImageField(upload_to='photo/%Y/%m/%d', blank = True)
    screen_name = models.CharField(max_length = 100, default = 'anon')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
    	return self.screen_name