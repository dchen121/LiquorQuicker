from django.db import models
from django.contrib.auth.models import AbstractUser


class LQUser(AbstractUser):
	avitar = models.ImageField('photos/%Y/%m/%d')
