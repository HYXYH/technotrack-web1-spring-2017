from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import os


def get_image_path(instance, filename):
    return os.path.join('posts', str(instance.id), 'img {}'.format(os.path.splitext(filename)[1]))


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blogs')
    name = models.CharField(max_length=100, default='noname blog')
    image = models.FileField(upload_to=get_image_path, default='default_images/no_post_image.jpg')
    description_title = models.CharField(max_length=100, default=' ')
    text = models.TextField(default=' ')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
#   tags


class Post(models.Model):
    blog = models.ForeignKey(Blog, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    image = models.FileField(upload_to=get_image_path, default='default_images/no_post_image.jpg')
    title = models.CharField(max_length=100)
    description_title = models.CharField(max_length=100, default=' ')
    text = models.TextField(default=' ')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
#   tags
