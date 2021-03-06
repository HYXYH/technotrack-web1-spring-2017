from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Comment(models.Model):
    post = models.ForeignKey('blogpost.Post', related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        result = '{0} {1} {2}: {3}'.format(
            self.created_at.ctime(),
            self.author.first_name,
            self.author.last_name,
            self.text[:30])
        return result

    class Meta:
        ordering = ['created_at']