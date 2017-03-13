from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

import os


def get_avatar_path(instance, filename):
    return os.path.join('avatars', 'user' + str(instance.id), 'ava' + os.path.splitext(filename)[1])


class User(AbstractUser):

    avatar = models.ImageField(upload_to=get_avatar_path, default='default_images/no_avatar.png')
    site = models.CharField( max_length=50, blank=True)
