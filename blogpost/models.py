# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import os

from django.core.cache import caches
cache = caches['default']


def get_image_path(instance, filename):
    if hasattr(instance, 'blog'):
        return os.path.join('posts', str(instance.id), 'img {}'.format(os.path.splitext(filename)[1]))
    return os.path.join('blogs', str(instance.id), 'img {}'.format(os.path.splitext(filename)[1]))


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


class BlogQueryset(models.QuerySet):

    def annotate_everything(self):
        qs = self.select_related('author')
        qs = qs.prefetch_related('categories')

        #fixme: почему-то нормально считаются только комменты
        qs = qs.annotate(post_count=models.Count('posts'),
                         comment_count=models.Count('posts__comments'),
                         rate=models.Sum(models.F('posts__rate')))
        return qs


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blogs')
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to=get_image_path, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='blogs')

    objects = BlogQueryset.as_manager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class PostQueryset(models.QuerySet):

    def annotate_everything(self):
        qs = self.select_related('author')
        qs = qs.prefetch_related('comments', 'comments__author')
        return qs

    def posts_for_user(self, user):
        return self.filter((models.Q(is_draft=False) | models.Q(author=user)))

    def get_likes(self):
        nolikes = []
        for post in self:
            cache_key = 'post{}likescount'.format(post.id)
            likes_count = cache.get(cache_key)
            if likes_count is None:
                nolikes.append(post.id)
            else:
                post.likes_count = likes_count

        qs_to_cache = Post.objects.filter(id__in=nolikes).annotate(likes_count=models.Sum('rate'))
        for post in qs_to_cache:
            cache_key = 'post{}likescount'.format(post.id)
            cache.set(cache_key, post.likes_count, 10)
        return self


class Post(models.Model):
    blog = models.ForeignKey(Blog, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    image = models.FileField(upload_to=get_image_path, null=True, blank=True)
    title = models.CharField(max_length=100)
    description_title = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_draft = models.BooleanField(default=False)

    objects = PostQueryset.as_manager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
#   tags


class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='liked')
    post = models.ForeignKey(Post, related_name='likers')
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
