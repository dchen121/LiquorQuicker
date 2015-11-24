from django.db import models
from django.contrib.auth.models import AbstractUser

from Map.models import LiquorLocation, BCLiquor


def avatar_directory_path(instance, filename):
    #TODO: clean this up should be in the LQUser class
    return 'profile/{0}'.format(instance.username)


class LQUser(AbstractUser):
    """
    A custom User model which includes a avatar field for a user image
    """
    avatar = models.ImageField(upload_to=avatar_directory_path, blank=True)
    favorite_store = models.ForeignKey(LiquorLocation, null=True)
    favorite_bev = models.ForeignKey(BCLiquor, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username
