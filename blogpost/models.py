from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import os


def get_image_path(instance, filename):
    return os.path.join('posts', str(instance.id), 'img {}'.format(os.path.splitext(filename)[1]))


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    color_choises = (
        ('label-default', 'gray'),
        ('label-primary', 'blue'),
        ('label-success', 'green'),
        ('label-info', 'cyan'),
        ('label-warning', 'orange'),
        ('label-danger', 'red'),
    )
    color = models.CharField(max_length=15, choices=color_choises, default='label-default')

    def __unicode__(self):
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blogs')
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to=get_image_path, null=True, blank=True)
    description_title = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='blogs')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
#   tags


class Post(models.Model):
    blog = models.ForeignKey(Blog, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    image = models.FileField(upload_to=get_image_path, null=True, blank=True)
    title = models.CharField(max_length=100)
    description_title = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
#   tags
